# SSH Configuration Hardening - Task 5

## 📊 Before vs After Comparison

### ❌ INSECURE Configuration (Before)

```bash
Protocol 1,2              # Allows insecure Protocol 1
PermitRootLogin yes       # Root can login directly
PasswordAuthentication yes # Allows password-based auth
PermitEmptyPasswords yes  # Allows empty passwords!
PubkeyAuthentication yes  # Key auth enabled (good)
X11Forwarding yes         # X11 forwarding enabled
Port 22                   # Standard port
```

### ✅ HARDENED Configuration (After)

```bash
Protocol 2                # Only secure Protocol 2
PermitRootLogin no        # Root login disabled
PasswordAuthentication no # Only key-based auth
PermitEmptyPasswords no   # Empty passwords forbidden
PubkeyAuthentication yes  # Key auth enabled
X11Forwarding no          # X11 disabled (reduces attack surface)
Port 22                   # Standard port
```

---

## 🔒 Security Issues Fixed

### 1. **Protocol 1 Removed** ⚠️ CRITICAL
**Issue:** SSH Protocol 1 has known vulnerabilities and weaknesses
- Man-in-the-middle attacks
- Weak encryption algorithms
- Session hijacking vulnerabilities

**Fix:** `Protocol 2`
- Protocol 2 has stronger encryption
- Better key exchange mechanisms
- Industry standard since 2006

---

### 2. **Root Login Disabled** ⚠️ CRITICAL
**Issue:** `PermitRootLogin yes` allows direct root access
- Attackers know the username (root)
- Only need to brute force the password
- No audit trail of who used root
- Increases attack surface

**Fix:** `PermitRootLogin no`
- Forces users to login as normal users
- Use `sudo` for privileged operations
- Better accountability and logging
- Follows principle of least privilege

---

### 3. **Password Authentication Disabled** ⚠️ HIGH
**Issue:** `PasswordAuthentication yes` allows password-based login
- Vulnerable to brute force attacks
- Weak passwords can be guessed
- Passwords can be intercepted or stolen
- Dictionary attacks

**Fix:** `PasswordAuthentication no`
- Only SSH key-based authentication allowed
- Much stronger cryptographic authentication
- Keys are typically 2048-4096 bits
- Immune to brute force password attacks

---

### 4. **Empty Passwords Forbidden** ⚠️ CRITICAL
**Issue:** `PermitEmptyPasswords yes` allows accounts with no password
- Anyone can login to accounts without passwords
- Complete security bypass
- Trivial to exploit

**Fix:** `PermitEmptyPasswords no`
- All accounts must have authentication
- No passwordless access

---

### 5. **X11 Forwarding Disabled** ⚠️ MEDIUM
**Issue:** `X11Forwarding yes` enables X11 protocol forwarding
- Increases attack surface
- Can be exploited for privilege escalation
- Allows GUI applications over SSH
- Not needed in most server environments

**Fix:** `X11Forwarding no`
- Reduces attack surface
- Only enable if specifically needed
- Most servers don't need GUI forwarding

---

## 🛡️ Additional Security Enhancements

Beyond fixing the obvious issues, the hardened config adds:

### 6. **Limit Authentication Attempts**
```bash
MaxAuthTries 3
```
- Limits failed login attempts
- Prevents brute force attacks
- Disconnects after 3 failed attempts

### 7. **Strong Cryptography**
```bash
Ciphers aes256-ctr,aes192-ctr,aes128-ctr
MACs hmac-sha2-512,hmac-sha2-256
```
- Only allow strong encryption ciphers
- Use secure message authentication codes
- Disable weak/deprecated algorithms

### 8. **Disable Unused Authentication Methods**
```bash
ChallengeResponseAuthentication no
KerberosAuthentication no
GSSAPIAuthentication no
HostbasedAuthentication no
```
- Reduces attack surface
- Only enable what you need
- Each disabled service is one less vulnerability

### 9. **Session Management**
```bash
ClientAliveInterval 300
ClientAliveCountMax 2
LoginGraceTime 60
```
- Disconnects idle sessions (5 minutes)
- Prevents abandoned sessions
- Limits login time to 60 seconds

### 10. **Enhanced Logging**
```bash
LogLevel VERBOSE
```
- Better audit trail
- Helps detect attacks
- Compliance requirements

### 11. **Disable Forwarding (if not needed)**
```bash
AllowTcpForwarding no
AllowAgentForwarding no
```
- Prevents SSH tunneling abuse
- Reduces attack surface
- Enable only if required

---

## 📚 Best Practices Summary

### ✅ Do:
1. ✅ Use SSH Protocol 2 only
2. ✅ Disable root login
3. ✅ Use key-based authentication
4. ✅ Limit authentication attempts
5. ✅ Use strong ciphers and MACs
6. ✅ Enable verbose logging
7. ✅ Set session timeouts
8. ✅ Regularly update SSH software
9. ✅ Use AllowUsers/AllowGroups to restrict access
10. ✅ Consider changing default port (security through obscurity)

### ❌ Don't:
1. ❌ Use Protocol 1
2. ❌ Allow root login
3. ❌ Allow password authentication
4. ❌ Allow empty passwords
5. ❌ Enable unnecessary features (X11, TCP forwarding)
6. ❌ Use weak ciphers
7. ❌ Allow unlimited authentication attempts
8. ❌ Leave default settings without review

---

## 🔍 Verification Commands

After applying the hardened configuration:

```bash
# Check SSH configuration syntax
sudo sshd -t -f 5-sshd_config

# View effective SSH configuration
sudo sshd -T -f 5-sshd_config

# Check specific settings
sudo sshd -T -f 5-sshd_config | grep -E "protocol|permitrootlogin|passwordauth"

# Test SSH connection (from another terminal first!)
ssh -v user@localhost

# Check SSH logs
sudo tail -f /var/log/auth.log
```

---

## 📖 References

- `man sshd_config` - Complete SSH daemon configuration manual
- [OpenSSH Security Guidelines](https://www.openssh.com/security.html)
- [NIST SSH Guidelines](https://nvlpubs.nist.gov/nistpubs/ir/2015/NIST.IR.7966.pdf)
- [CIS Benchmark for SSH](https://www.cisecurity.org/)
- [Mozilla SSH Guidelines](https://infosec.mozilla.org/guidelines/openssh)

---

## 🎯 Learning Outcomes

By completing this task, you've learned:

1. ✅ How to identify insecure SSH configurations
2. ✅ SSH security best practices
3. ✅ The importance of key-based authentication
4. ✅ Attack surface reduction principles
5. ✅ Defense in depth strategies
6. ✅ How to read and modify sshd_config
7. ✅ The difference between SSH Protocol 1 and 2
8. ✅ Why disabling root login is critical

---

## ⚠️ Important Notes

**Before applying to production:**

1. **Test in a safe environment first**
2. **Keep a terminal session open** before restarting SSH
3. **Have console/physical access** in case of lockout
4. **Backup original configuration**: `cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup`
5. **Test with a new session** before closing current one
6. **Ensure you have SSH keys set up** before disabling passwords
7. **Document your changes**

**Apply configuration:**
```bash
# Copy to system location
sudo cp 5-sshd_config /etc/ssh/sshd_config

# Test configuration
sudo sshd -t

# Restart SSH service (keep current session open!)
sudo systemctl restart sshd
# OR
sudo service ssh restart
```

---

## 📈 Security Impact Assessment

| Setting | Before | After | Risk Reduction |
|---------|--------|-------|----------------|
| Protocol | 1,2 | 2 only | 🔴 HIGH → 🟢 LOW |
| Root Login | Allowed | Denied | 🔴 CRITICAL → 🟢 LOW |
| Password Auth | Allowed | Denied | 🔴 HIGH → 🟢 LOW |
| Empty Passwords | Allowed | Denied | 🔴 CRITICAL → 🟢 LOW |
| X11 Forwarding | Enabled | Disabled | 🟡 MEDIUM → 🟢 LOW |

**Overall Security Improvement:** 🔴 CRITICAL RISK → 🟢 LOW RISK

---

**Task Completed!** ✅

The hardened SSH configuration is now saved in `5-sshd_config` and ready to be pushed to the repository.
