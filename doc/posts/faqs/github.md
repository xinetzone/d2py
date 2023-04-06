```{post} 2023/04/06 08:00
:category: GitHub
:tags: FAQs
:excerpt: 1
```

# GitHub 常见错误

## gnutls_handshake() failed: The TLS connection was non-properly terminated.

解决措施（重置代理）：

```bash
git config --global  --unset https.https://github.com.proxy 
git config --global  --unset http.https://github.com.proxy 
```
