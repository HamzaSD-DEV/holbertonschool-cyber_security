#!/bin/bash
# Usage: ./0-whois.sh domain.com
# Produces domain.com.csv with contact info in CSV format as required.

whois "$1" | awk '
BEGIN {
    FS = ": "; OFS = ",";
}
function trim(s) { sub(/^[ \t\r\n]+/, "", s); sub(/[ \t\r\n]+$/, "", s); return s }
function add_field(prefix, field, val,   key) {
    key = prefix " " field;
    if (field == "Street") {
        # Concatenate multiple Street lines with a space
        if (key in data && length(data[key])) {
            data[key] = data[key] " " trim(val);
        } else {
            data[key] = trim(val);
        }
    } else {
        data[key] = trim(val);
    }
}
/^(Registrant|Admin|Tech) / {
    # Split only at the first occurrence of ": " to preserve values containing ":"
    header = $1; value = $2;
    # In case there are more than two fields due to additional colons in value, rebuild value
    if (NF > 2) {
        for (i = 3; i <= NF; i++) value = value ": " $i;
    }
    split(header, b, " ");
    prefix = b[1];
    field = substr(header, length(prefix) + 2); # rest of header after the space
    add_field(prefix, field, value);
}
END {
    sections[1] = "Registrant"; sections[2] = "Admin"; sections[3] = "Tech";
    fields[1] = "Name";
    fields[2] = "Organization";
    fields[3] = "Street";
    fields[4] = "City";
    fields[5] = "State/Province";
    fields[6] = "Postal Code";
    fields[7] = "Country";
    fields[8] = "Phone";
    fields[9] = "Phone Ext";
    fields[10] = "Fax";
    fields[11] = "Fax Ext";
    fields[12] = "Email";

    first = 1;
    for (si = 1; si <= 3; si++) {
        p = sections[si];
        for (fi = 1; fi <= 12; fi++) {
            f = fields[fi];
            key = p " " f;
            val = data[key];
            # Add a trailing space for Street field if non-empty
            if (f == "Street" && length(val)) {
                outval = val " ";
            } else {
                outval = val;
            }
            # For Ext fields include colon in header
            label = (f == "Phone Ext" || f == "Fax Ext") ? p " " f ":" : p " " f;
            line = label "," outval;
            if (first) { printf "%s", line; first = 0 } else { printf "\n%s", line }
        }
    }
    # End with a single newline (not an extra blank line)
    printf "\n";
}
' > "$1.csv"
