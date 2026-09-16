<!-- owner: engineering -->
# TESTING

TDD 铁律与四步走验证。

TDD 铁律：无失败测试不写生产代码。所有有运行时行为、被用户依赖的代码（含 AI 生成）必须走 RED-GREEN-REFACTOR。
不强制 TDD：工具链自动生成的中间代码（protobuf、Prisma client、codegen 产物）、纯 schema/配置、一次性 throwaway 原型。
每个 Phase 必过四步走验证：Code Review、测试完整性（含 TDD 合规）、编译验证、功能测试，全通过才算完成。
详细：dev-builder SKILL.md 写 TDD 纪律，bug-fixer 写复现测试纪律，code-review Stage 2 写 TDD 合规检查。方法论锚点 superpowers:test-driven-development、systematic-debugging、verification-before-completion。

<!-- owner: engineering -->
