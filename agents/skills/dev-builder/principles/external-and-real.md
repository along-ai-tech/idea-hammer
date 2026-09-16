# 原则：SDK-First + 联网优先 + 真实优先

> 框架和 SDK 已有的能力不重复造；用外部库/API 前先 WebSearch 确认当前版本用法；按钮/数字/卡片必须代表真实数据和真实行为。

## SDK-First

- 框架和 SDK 已有的能力不重复造，用之前先确认

## 联网优先

- 用外部库、API 前先 WebSearch 确认当前版本用法，不靠过期记忆

## 真实优先

- 按钮、数字、卡片必须代表真实数据和真实行为
- 不写死、不假数据、不留装饰
- 引入项目里零先例的 UI 元素前先 grep 全项目确认先例，零先例默认不引入

## 落地指引

泛原则需要落地时，参考：
- 库选哪个 → `_engineering-constraints/ecosystem-matrix/`
- 不能造什么 → `_engineering-constraints/anti-reinvent/`
- 语言规范 → `_engineering-constraints/coding-style/`
