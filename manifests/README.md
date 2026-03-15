# Kubernetes Secret 配置指南

## 概述

本目录包含 Rambutan 服务的 Kubernetes 部署配置。敏感凭证（如阿里云 OSS AccessKey）存储在 Kubernetes Secret 中，而不是硬编码在 YAML 文件中。

## Secret 命名

每个 namespace 中创建的 Secret 名称为 `rambutan-secret`。

## 创建 Secret

在每个 namespace 中执行以下命令：

```bash
# v namespace
kubectl create secret generic rambutan-secret \
  --from-literal=access-key-id='YOUR_ACCESS_KEY_ID' \
  --from-literal=access-key-secret='YOUR_ACCESS_KEY_SECRET' \
  -n v

# w namespace
kubectl create secret generic rambutan-secret \
  --from-literal=access-key-id='YOUR_ACCESS_KEY_ID' \
  --from-literal=access-key-secret='YOUR_ACCESS_KEY_SECRET' \
  -n w

# www namespace
kubectl create secret generic rambutan-secret \
  --from-literal=access-key-id='YOUR_ACCESS_KEY_ID' \
  --from-literal=access-key-secret='YOUR_ACCESS_KEY_SECRET' \
  -n www
```

## 验证 Secret

```bash
kubectl get secret rambutan-secret -n <namespace>
```

## 更新 Secret

如果需要更新凭证：

```bash
kubectl delete secret rambutan-secret -n <namespace>
kubectl create secret generic rambutan-secret \
  --from-literal=access-key-id='NEW_ACCESS_KEY_ID' \
  --from-literal=access-key-secret='NEW_ACCESS_KEY_SECRET' \
  -n <namespace>
```

或者使用 `kubectl apply` 配合 YAML 文件（base64 编码值）。

## 环境变量

Deployment 会从 Secret 读取以下环境变量：

- `OSS_ACCESS_KEY_ID` - 阿里云 AccessKey ID
- `OSS_ACCESS_KEY_SECRET` - 阿里云 AccessKey Secret
