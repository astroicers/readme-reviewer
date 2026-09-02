# widgetctl — 一行把 widget 部署到 k8s

給**已經有 k8s 叢集、不想手寫 manifest** 的人。不適合單機開發(見「什麼時候別用」)。

## 安裝

需要 Go 1.21+ 與可用的 `kubectl` context。

```bash
go install github.com/example/widgetctl@latest
widgetctl version   # 應印出 widgetctl v1.4.0
```

## 使用

```bash
widgetctl deploy ./widget.yaml --namespace prod
```

成功時會印:

```text
✓ applied 3 resources to prod
```

## 為什麼不用 Helm

Helm 的 template 在**跨環境差異只有兩三個欄位**時,維護成本高於收益 ——
本工具走「一份 yaml + 覆寫」而非 template,理由是 debug 時看得到最終結果。

## 什麼時候別用

- 單機/minikube 開發:直接 `kubectl apply` 更快
- 需要 chart 生態系(依賴管理、repo)時:用 Helm

## 已知限制

- 只支援 apps/v1 的 Deployment 與 Service(**驗證於 2026-08,k8s 1.30**)
- 不做 rollback,失敗請自行 `kubectl rollout undo`

詳見 [設計說明](#為什麼不用-helm)。

## 求助與維護

- 問題先看[已知限制](#已知限制),再開 [GitHub Issues](https://example.com/issues)
- 維護者:platform 團隊(`#platform` 頻道可敲)
