# Peekaboo 文档索引 (TOC)

本文档汇总了 Peekaboo 所有参考手册的摘要，用于快速定位功能说明。

## peekaboo/ARCHITECTURE.md

```yaml
summary: 'Review Peekaboo Architecture Overview guidance'
read_when:
  - 'planning work related to peekaboo architecture overview'
  - 'debugging or extending features described here'
```

## peekaboo/AppKit-Implementing-Liquid-Glass-Design.md

```yaml
summary: 'Review Implementing Liquid Glass Design in AppKit guidance'
read_when:
  - 'planning work related to implementing liquid glass design in appkit'
  - 'debugging or extending features described here'
```

## peekaboo/MCP.md

```yaml
summary: 'Review Model Context Protocol (MCP) in Peekaboo guidance'
read_when:
  - 'planning work related to model context protocol (mcp) in peekaboo'
  - 'debugging or extending features described here'
```

## peekaboo/README.md

```yaml
summary: 'Peekaboo documentation map'
read_when:
  - 'finding the right Peekaboo doc quickly'
  - 'onboarding or sharing docs with teammates'
```

## peekaboo/RELEASING.md

```yaml
summary: 'Peekaboo 3.x release checklist (main repo + submodules)'
read_when:
  - 'preparing for a release'
  - 'cleaning up repos before release'
```

## peekaboo/SwiftUI-Implementing-Liquid-Glass-Design.md

```yaml
summary: 'Review Implementing Liquid Glass Design in SwiftUI guidance'
read_when:
  - 'planning work related to implementing liquid glass design in swiftui'
  - 'debugging or extending features described here'
```

## peekaboo/SwiftUI-New-Toolbar-Features.md

```yaml
summary: 'Review SwiftUI New Toolbar Features guidance'
read_when:
  - 'planning work related to swiftui new toolbar features'
  - 'debugging or extending features described here'
```

## peekaboo/TODO.md

```yaml
summary: Track backlog of Peekaboo feature ideas and automations under consideration
read_when:
  - reviewing or grooming upcoming Peekaboo features
  - adding new automation ideas or evaluating feasibility
```

## peekaboo/agent-chat.md

```yaml
summary: 'Document the minimal interactive chat loop for peekaboo agent'
read_when:
  - 'planning work related to the agent chat loop'
  - 'debugging or extending the interactive agent shell'
```

## peekaboo/agent-patterns.md

```yaml
summary: 'Review Agent Patterns Documentation guidance'
read_when:
  - 'planning work related to agent patterns documentation'
  - 'debugging or extending features described here'
```

## peekaboo/application-resolving.md

```yaml
summary: 'Review Application Resolution in Peekaboo guidance'
read_when:
  - 'planning work related to application resolution in peekaboo'
  - 'debugging or extending features described here'
```

## peekaboo/audio.md

```yaml
summary: 'Review Audio Architecture guidance'
read_when:
  - 'planning work related to audio architecture'
  - 'debugging or extending features described here'
```

## peekaboo/bridge-host.md

```yaml
summary: "Describe Peekaboo Bridge host architecture (socket-based TCC broker)"
read_when:
  - "embedding Peekaboo automation into another macOS app"
  - "debugging remote execution for Peekaboo CLI"
  - "auditing auth/security for privileged automation surfaces"
```

## peekaboo/building.md

```yaml
summary: 'How to build Peekaboo from source, run release scripts, and use the Poltergeist watcher.'
read_when:
  - 'compiling the CLI locally'
  - 'prepping release artifacts or tweaking Poltergeist workflows'
```

## peekaboo/claude-hooks.md

```yaml
summary: 'Claude Code pre-command hooks for git safety'
read_when:
  - Setting up git protection for AI agents
  - Debugging blocked git commands
  - Understanding hook behavior
```

## peekaboo/cli-command-reference.md

```yaml
summary: 'Cheat sheet for every Peekaboo CLI command grouped by category.'
read_when:
  - 'learning what each CLI subcommand does'
  - 'mapping agent tools to direct CLI usage'
```

## peekaboo/clipboard.md

```yaml
summary: 'Design for unified clipboard tool (CLI + MCP) covering text, images, files, and raw data'
read_when:
  - 'planning or implementing the peekaboo clipboard command/tool'
  - 'debugging clipboard read/write behaviors or size limits'
```

## peekaboo/commander.md

```yaml
summary: 'Commander CLI parsing redesign for Peekaboo'
read_when:
  - Replacing ArgumentParser in the CLI
  - Touching Peekaboo command-line parsing/runtime code
```

## peekaboo/concurrency.md

```yaml
summary: 'Practical guide to Swift 6.2 approachable concurrency'
read_when:
  - Enabling default actor isolation in a target
  - Deciding where to use @concurrent or nonisolated async
```

## peekaboo/configuration.md

```yaml
summary: 'Reference for Peekaboo configuration precedence, environment variables, and credential handling.'
read_when:
  - 'setting environment variables or editing ~/.peekaboo/config.json'
  - 'debugging why CLI settings are not applied'
```

## peekaboo/daemon.md

```yaml
summary: 'Plan for a headless Peekaboo daemon with live window tracking and MCP integration'
read_when:
  - 'planning or implementing the Peekaboo daemon lifecycle'
  - 'adding live window tracking or daemon status reporting'
  - 'wiring MCP to run in daemon mode'
```

## peekaboo/engine.md

```yaml
summary: "Capture engine selector (ScreenCaptureKit vs CGWindowList) and how to control it."
read_when:
  - "changing capture behavior or debugging SC vs CG fallbacks"
  - "adding new commands that trigger screenshots"
```

## peekaboo/error-handling-guide.md

```yaml
summary: 'Review Peekaboo Error Handling Guide guidance'
read_when:
  - 'planning work related to peekaboo error handling guide'
  - 'debugging or extending features described here'
```

## peekaboo/focus.md

```yaml
summary: 'Review Window Focus and Space Management guidance'
read_when:
  - 'planning work related to window focus and space management'
  - 'debugging or extending features described here'
```

## peekaboo/homebrew-setup.md

```yaml
summary: 'Review Setting Up Homebrew Tap for Peekaboo guidance'
read_when:
  - 'planning work related to setting up homebrew tap for peekaboo'
  - 'debugging or extending features described here'
```

## peekaboo/human-mouse-move.md

```yaml
summary: 'How Peekaboo generates natural-looking cursor motion'
read_when:
  - 'tuning mouse movement heuristics'
  - 'debugging human-style pointer paths'
```

## peekaboo/human-typing.md

```yaml
summary: 'Plan for Peekaboo\'s human-like typing cadence'
read_when:
  - 'designing or tuning TypeCommand/TypeTool timing controls'
  - 'implementing Peekaboo automation that must mimic human keystrokes'
```

## peekaboo/install-mcp-claude-desktop.md

```yaml
summary: 'Review Installing Peekaboo MCP in Claude Desktop guidance'
read_when:
  - 'planning work related to installing peekaboo mcp in claude desktop'
  - 'debugging or extending features described here'
```

## peekaboo/logging-guide.md

```yaml
summary: 'Review Peekaboo Logging Guide guidance'
read_when:
  - 'planning work related to peekaboo logging guide'
  - 'debugging or extending features described here'
```

## peekaboo/manual-testing.md

```yaml
summary: 'Manual MCP smoke tests via mcporter for Peekaboo'
read_when:
  - 'verifying Peekaboo MCP server changes or regressions'
  - 'running hand-driven MCP smokes before releases'
```

## peekaboo/mcp-best-practices.md

```yaml
summary: 'Review MCP Best Practices - May 26, 2025 guidance'
read_when:
  - 'planning work related to mcp best practices - may 26, 2025'
  - 'debugging or extending features described here'
```

## peekaboo/mcp-testing.md

```yaml
summary: 'Review MCP Server Testing Guide guidance'
read_when:
  - 'planning work related to mcp server testing guide'
  - 'debugging or extending features described here'
```

## peekaboo/modern-api.md

```yaml
summary: 'Review Modern Tachikoma API Design & Migration Plan guidance'
read_when:
  - 'planning work related to modern tachikoma api design & migration plan'
  - 'debugging or extending features described here'
```

## peekaboo/modern-swift.md

```yaml
summary: 'Review Modern Swift Development guidance'
read_when:
  - 'planning work related to modern swift development'
  - 'debugging or extending features described here'
```

## peekaboo/module-architecture-refactoring.md

```yaml
summary: 'Review Module Architecture Refactoring Plan guidance'
read_when:
  - 'planning work related to module architecture refactoring plan'
  - 'debugging or extending features described here'
```

## peekaboo/module-refactoring-example.md

```yaml
summary: 'Review Module Refactoring: Practical Example guidance'
read_when:
  - 'planning work related to module refactoring: practical example'
  - 'debugging or extending features described here'
```

## peekaboo/oauth.md

```yaml
summary: 'How Peekaboo handles OAuth for OpenAI/Codex and Anthropic (Claude Pro/Max)'
read_when:
  - 'adding or debugging OAuth logins for OpenAI or Anthropic'
  - 'explaining where tokens are stored and how they refresh'
```

## peekaboo/permissions.md

```yaml
summary: 'Grant required macOS permissions and understand performance trade-offs for Peekaboo.'
read_when:
  - 'Peekaboo cannot capture screens or focus windows'
  - 'tuning capture performance or troubleshooting permission dialogs'
```

## peekaboo/playground-testing.md

```yaml
summary: 'Review Peekaboo Playground Testing Methodology guidance'
read_when:
  - 'planning work related to peekaboo playground testing methodology'
  - 'debugging or extending features described here'
```

## peekaboo/poltergeist.md

```yaml
summary: 'Poltergeist usage, migration highlights, and watchman exclusion tips'
read_when:
  - Tuning local rebuild performance
  - Disabling specific Poltergeist targets
  - Debugging CLI vs. mac app rebuilds
  - Migrating Poltergeist configs or tightening Watchman excludes
```

## peekaboo/provider.md

```yaml
summary: 'Review Custom AI Provider Configuration guidance'
read_when:
  - 'planning work related to custom ai provider configuration'
  - 'debugging or extending features described here'
```

## peekaboo/refactor.md

```yaml
summary: 'Runtime logger + Visualizer refactor log'
read_when:
  - Coordinating CLI runtime injection
  - Tracking Visualizer client fixes
```

## peekaboo/remote-testing.md

```yaml
summary: 'Review Remote Testing Playbook guidance'
read_when:
  - 'planning work related to remote testing playbook'
  - 'debugging or extending features described here'
```

## peekaboo/restore.md

```yaml
summary: 'Checklist for recreating the lost CLI/Visualizer refactor'
read_when:
  - Repo changes vanished after a reset
  - Coordinating manual restoration of CLI runtime refactor
  - Hunting for the Visualizer resiliency patches
```

## peekaboo/security.md

```yaml
summary: 'Security and tool hardening guide for Peekaboo'
read_when:
  - 'tightening or auditing allowed tools/providers'
  - 'running Peekaboo in untrusted contexts and need safe defaults'
```

## peekaboo/service-api-reference.md

```yaml
summary: 'Review PeekabooCore Service API Reference guidance'
read_when:
  - 'planning work related to peekaboocore service api reference'
  - 'debugging or extending features described here'
```

## peekaboo/silgen-crash-debug.md

```yaml
summary: 'Playbook for debugging Swift SILGen compiler crashes during automation tests'
read_when:
  - 'stuck on fatal Swift compiler signals (5/6/11) building CLI tests'
  - 'trying to minimize repros before filing bugs with Apple'
```

## peekaboo/skylight-spaces-api.md

```yaml
summary: 'Review ifndef CGS_ACCESSIBILITY_INTERNAL_H guidance'
read_when:
  - 'planning work related to ifndef cgs_accessibility_internal_h'
  - 'debugging or extending features described here'
```

## peekaboo/spec.md

```yaml
summary: 'Review Peekaboo 3.0 System Specification guidance'
read_when:
  - 'planning work related to peekaboo 3.0 system specification'
  - 'debugging or extending features described here'
```

## peekaboo/swift-6.2-compiler-crash.md

```yaml
summary: 'Review Swift 6.2 CLI Compiler Crash Notes guidance'
read_when:
  - 'planning work related to swift 6.2 cli compiler crash notes'
  - 'debugging or extending features described here'
```

## peekaboo/swift-module-plan.md

```yaml
summary: 'Review Swift Module Architecture Plan guidance'
read_when:
  - 'planning work related to swift module architecture plan'
  - 'debugging or extending features described here'
```

## peekaboo/swift-performance.md

```yaml
summary: 'Review Swift Build Performance Optimization Guide guidance'
read_when:
  - 'planning work related to swift build performance optimization guide'
  - 'debugging or extending features described here'
```

## peekaboo/swift-subprocess.md

```yaml
summary: 'Review swift-subprocess Adoption Guide guidance'
read_when:
  - 'planning work related to swift-subprocess adoption guide'
  - 'debugging or extending features described here'
```

## peekaboo/swift-testing-playbook.md

```yaml
summary: "The Ultimate Swift Testing Playbook (2024 WWDC Edition, expanded with Apple docs from June 2025)"
read_when:
  - Working on the ultimate swift testing playbook (2024 wwdc edition, expanded with apple docs from june 2025) topics
```

## peekaboo/swift6-migration-compact.md

```yaml
summary: 'Review The Swift Concurrency Migration Guide guidance'
read_when:
  - 'planning work related to the swift concurrency migration guide'
  - 'debugging or extending features described here'
```

## peekaboo/test-refactor.md

```yaml
summary: 'Review Test Refactor Task List guidance'
read_when:
  - 'planning work related to test refactor task list'
  - 'debugging or extending features described here'
```

## peekaboo/tool-formatter-architecture.md

```yaml
summary: 'Review Tool Formatter Architecture guidance'
read_when:
  - 'planning work related to tool formatter architecture'
  - 'debugging or extending features described here'
```

## peekaboo/tui.md

```yaml
summary: 'Review Terminal Output Modes and Progressive Enhancement guidance'
read_when:
  - 'planning work related to terminal output modes and progressive enhancement'
  - 'debugging or extending features described here'
```

## peekaboo/visualizer.md

```yaml
summary: 'Peekaboo visual feedback architecture, animation catalog, and diagnostics'
read_when:
  - Designing or debugging visualizer animations
  - Touching visual feedback settings or transport code
  - Investigating CLI → app visual feedback issues
```

## peekaboo/window-screenshot-smart-select.md

```yaml
summary: 'Heuristics for filtering CG windows before screenshotting'
read_when:
  - 'touching ImageCommand/SeeCommand window selection logic'
  - 'plumbing CGWindow metadata into ServiceWindowInfo'
  - 'debugging why peekaboo image skips or captures overlays'
```

## peekaboo/research/agentic.md

```yaml
summary: 'Agentic improvements: desktop context injection, tool gating, and verification loops (research + plan)'
read_when:
  - 'planning improvements to Peekaboo agent runtime'
  - 'auditing prompt-injection risks from desktop context'
  - 'wiring verification/smart-capture into tool execution'
```

## peekaboo/research/browser.md

```yaml
summary: 'Notes on DOM/JavaScript automation options for existing browser windows.'
read_when:
  - 'designing Peekaboo browser automation features'
  - 'evaluating DOM access strategies beyond AX'
```

## peekaboo/research/intelligent-build-prioritization.md

```yaml
summary: 'Review Intelligent Build Prioritization guidance'
read_when:
  - 'planning work related to intelligent build prioritization'
  - 'debugging or extending features described here'
```

## peekaboo/research/interaction-debugging.md

```yaml
summary: 'Track active interaction-layer bugs and reproduction steps'
read_when:
  - Debugging CLI interaction regressions
  - Triaging Peekaboo automation failures
```

## peekaboo/logging-profiles/README.md

```yaml
summary: 'Review Peekaboo Logging - Fixing macOS Log Privacy Redaction guidance'
read_when:
  - 'planning work related to peekaboo logging - fixing macos log privacy redaction'
  - 'debugging or extending features described here'
```

## peekaboo/archive/refactor/README.md

```yaml
summary: 'Index of archived refactor logs (Nov 2025)'
read_when:
  - 'digging up historical refactor context'
  - 'continuing work referenced by past refactor logs'
```

## peekaboo/archive/refactor/agent-command-split.md

```yaml
summary: 'Notes from the Nov 17, 2025 AgentCommand split refactor'
read_when:
  - 'planning or reviewing AgentCommand refactors'
  - 'adding tests or UI glue around agent chat flows'
```

## peekaboo/archive/refactor/agent-improvements.md

```yaml
summary: "Borrowed improvements from pi-mono to harden and polish the Peekaboo agent"
read_when:
  - "planning agent runtime or CLI refactors"
  - "adding streaming/UI affordances to agent chat"
  - "rethinking session persistence, tool validation, or model selection"
```

## peekaboo/archive/refactor/axorcist-2025-11-19.md

```yaml
summary: "Working log for AXorcist boundary follow-ups (Nov 19, 2025)."
read_when:
  - "tracking AXorcist/Peekaboo accessibility refactor progress"
  - "assigning next tasks for AX toolkit/Peekaboo separation"
```

## peekaboo/archive/refactor/axorcist.md

```yaml
summary: "AXorcist↔Peekaboo boundary: keep AXorcist lean AX toolkit, push heuristics to Peekaboo; current state + next actions."
read_when:
  - "planning refactors that touch AXorcist or Peekaboo AX boundaries"
  - "deciding where AX and CG event helpers should live"
  - "adding or adjusting accessibility-related APIs"
```

## peekaboo/archive/refactor/capture-todo.md

```yaml
summary: 'Follow-ups after replacing watch with capture'
read_when:
  - 'planning capture feature work'
  - 'adding tests for capture live/video'
```

## peekaboo/archive/refactor/config-command-split.md

```yaml
summary: 'ConfigCommand split plan (Nov 17, 2025)'
read_when:
  - 'refactoring config CLI commands'
  - 'debugging ConfigCommand structure or runtime wiring'
```

## peekaboo/archive/refactor/config-refactor-2025-11-17.md

```yaml
summary: 'Config refactor notes (Nov 17, 2025)'
read_when:
  - 'continuing the config refactor'
  - 'debugging ConfigCommand behavior after Nov 2025 changes'
```

## peekaboo/archive/refactor/mcp-command-split.md

```yaml
summary: 'MCPCommand split notes (Nov 17, 2025)'
read_when:
  - 'refactoring MCP CLI commands or helpers'
  - 'aligning MCP subcommand formatting/error handling'
```

## peekaboo/archive/refactor/menu-service-refactor-2025-11-18.md

```yaml
summary: 'MenuService refactor notes (Nov 18, 2025)'
read_when:
  - 'continuing MenuService traversal/refactor work'
  - 'adding tests or diagnostics for menu interactions'
```

## peekaboo/archive/refactor/open-launch-tests.md

```yaml
summary: 'WIP notes for open/app launcher abstraction and test plan'
read_when:
  - 'resuming the open-command test/abstraction refactor'
  - 'continuing work on app launch --open behavior tests'
```

## peekaboo/archive/refactor/tool-results.md

```yaml
summary: 'Refactor tool results so agents can show rich, human-readable summaries'
read_when:
  - 'planning tool/agent runtime work'
  - 'touching ToolResponse or formatter plumbing'
```

## peekaboo/references/swift-testing-api.md

```yaml
summary: 'Apple Swift Testing API reference notes (llms-full excerpt)'
read_when:
  - 'reviewing Apple’s official Swift Testing API docs'
  - 'checking API details while implementing or debugging tests'
```

## peekaboo/references/swift62.md

```yaml
summary: 'Swift 6.2 upgrade notes for Peekaboo'
read_when:
  - 'upgrading toolchains or code to Swift 6.2'
  - 'debugging Swift 6.2 concurrency/warning changes in Peekaboo'
```

## peekaboo/providers/README.md

```yaml
summary: 'Index of AI provider docs (OpenAI, Anthropic, Grok, Ollama)'
read_when:
  - 'choosing or configuring AI providers for Peekaboo'
  - 'looking for provider-specific plans or status'
```

## peekaboo/providers/anthropic.md

```yaml
summary: 'Anthropic provider plan, status, and usage examples for Peekaboo'
read_when:
  - 'planning or extending Anthropic/Claude support'
  - 'debugging Anthropic provider behavior or SDK wiring'
  - 'needing CLI examples for Claude models'
```

## peekaboo/providers/grok.md

```yaml
summary: 'Review Grok 4 Implementation Guide for Peekaboo guidance'
read_when:
  - 'planning work related to grok 4 implementation guide for peekaboo'
  - 'debugging or extending features described here'
```

## peekaboo/providers/ollama-models.md

```yaml
summary: 'Review Ollama Models Guide guidance'
read_when:
  - 'planning work related to ollama models guide'
  - 'debugging or extending features described here'
```

## peekaboo/providers/ollama.md

```yaml
summary: 'Configure Peekaboo to use local Ollama models (llama3, llava, Ultrathink) and track the remaining implementation work.'
read_when:
  - 'running Peekaboo with local models'
  - 'debugging or extending the Ollama provider'
```

## peekaboo/providers/openai.md

```yaml
summary: 'OpenAI provider architecture and migration status in Peekaboo'
read_when:
  - 'debugging OpenAI model integration or tool calling'
  - 'planning changes to the OpenAI provider layer'
  - 'explaining the Assistants→Chat Completions migration'
```

## peekaboo/testing/tools.md

```yaml
summary: 'Systematic Peekaboo tool verification plan using Playground and file logs'
read_when:
  - 'planning or executing the comprehensive tool regression pass'
  - 'picking up the Playground-based test assignment'
```

## peekaboo/testing/trimmy.md

```yaml
summary: 'Manual Trimmy test plan using peekaboo clipboard'
read_when:
  - 'verifying Trimmy clipboard trimming behavior'
  - 'running manual clipboard regression tests'
```

## peekaboo/dev/menubar-timeouts.md

```yaml
summary: 'Troubleshoot menubar listing hangs/timeouts (AXorcist + MenuService fast path).'
read_when:
  - 'peekaboo list menubar hangs or times out'
  - 'debugging Accessibility traversal performance'
```

## peekaboo/commands/README.md

```yaml
summary: 'Index of Peekaboo CLI command docs'
read_when:
  - 'browsing available Peekaboo CLI commands'
  - 'linking to specific command docs'
```

## peekaboo/commands/agent.md

```yaml
summary: 'Drive Peekaboo’s autonomous agent via peekaboo agent'
read_when:
  - 'testing natural-language automation end-to-end'
  - 'resuming or debugging cached agent sessions'
```

## peekaboo/commands/app.md

```yaml
summary: 'Control macOS apps via peekaboo app'
read_when:
  - 'launching/quitting/focusing apps as part of an automation flow'
  - 'auditing running apps or force cycling foreground focus'
```

## peekaboo/commands/bridge.md

```yaml
summary: 'Diagnose Peekaboo Bridge host connectivity via peekaboo bridge'
read_when:
  - 'verifying whether the CLI is using Peekaboo.app / Clawdbot.app as a Bridge host'
  - 'debugging codesign / TeamID failures for bridge.sock connections'
  - 'checking which socket path Peekaboo is probing'
```

## peekaboo/commands/capture.md

```yaml
summary: 'Capture live screens/windows or ingest video; adaptive frames + contact sheet'
read_when:
  - 'using peekaboo capture'
  - 'automating long-running visual captures'
```

## peekaboo/commands/clean.md

```yaml
summary: 'Prune snapshot caches via peekaboo clean'
read_when:
  - 'saving disk space or nuking stale snapshot artifacts'
  - 'debugging interactions that still reference an old snapshot ID'
```

## peekaboo/commands/click.md

```yaml
summary: 'Target UI elements via peekaboo click'
read_when:
  - 'building deterministic element interactions after running `see`'
  - 'debugging focus/snapshot issues for click automation'
```

## peekaboo/commands/clipboard.md

```yaml
summary: 'Read/write the macOS clipboard via peekaboo clipboard'
read_when:
  - 'you need to seed or inspect clipboard content in automation flows'
  - 'saving/restoring the user clipboard around scripted actions'
```

## peekaboo/commands/config.md

```yaml
summary: 'Manage Peekaboo configuration and AI providers via peekaboo config'
read_when:
  - 'editing ~/.peekaboo/config.json or credentials safely'
  - 'adding/testing custom AI providers and API keys'
```

## peekaboo/commands/daemon.md

```yaml
summary: 'Start, stop, and inspect the headless Peekaboo daemon'
read_when:
  - 'managing the Peekaboo daemon lifecycle'
  - 'checking daemon health, permissions, or tracker status'
```

## peekaboo/commands/dialog.md

```yaml
summary: 'Handle macOS dialogs via peekaboo dialog'
read_when:
  - 'clicking buttons or entering text in save/open/system dialogs'
  - 'needing to inspect dialog structure for automation debugging'
```

## peekaboo/commands/dock.md

```yaml
summary: 'Automate macOS Dock interactions via peekaboo dock'
read_when:
  - 'launching/closing apps through Dock affordances'
  - 'toggling Dock visibility or iterating over Dock items in scripts'
```

## peekaboo/commands/drag.md

```yaml
summary: 'Execute drag-and-drop flows via peekaboo drag'
read_when:
  - 'moving elements/files with precision between apps or coordinates'
  - 'testing multi-step drags (Trash, Dock targets, selection gestures)'
```

## peekaboo/commands/hotkey.md

```yaml
summary: 'Send modifier combos via peekaboo hotkey'
read_when:
  - 'triggering Cmd-based shortcuts without scripting AppleScript'
  - 'validating that focus handling works before firing global hotkeys'
```

## peekaboo/commands/image.md

```yaml
summary: 'Capture raw screenshots or windows via peekaboo image'
read_when:
  - 'needing unannotated captures or multi-display exports'
  - 'pairing screenshots with inline AI analysis'
```

## peekaboo/commands/learn.md

```yaml
summary: 'Dump the full Peekaboo agent guide via peekaboo learn'
read_when:
  - 'needing the latest system prompt, tool catalog, and best practices in one blob'
  - 'building or QA-ing external agents that embed Peekaboo instructions'
```

## peekaboo/commands/list.md

```yaml
summary: 'Enumerate apps, windows, screens, and permissions via peekaboo list'
read_when:
  - 'inspecting what Peekaboo can currently target'
  - 'scripting toolchains that need structured app/window inventory'
```

## peekaboo/commands/mcp-capture-meta.md

```yaml
summary: 'MCP meta fields returned by the capture tool (live + video)'
read_when:
  - 'documenting agent-facing capture responses'
```

## peekaboo/commands/mcp.md

```yaml
summary: 'Run Peekaboo as an MCP server via peekaboo mcp'
read_when:
  - 'exposing Peekaboo as an MCP server'
  - 'debugging MCP server startup or transport options'
```

## peekaboo/commands/menu.md

```yaml
summary: 'Drive application menus via peekaboo menu'
read_when:
  - 'navigating File/Edit/... menus or menu extras without UI scripting'
  - 'listing menu trees to grab exact command paths for automation'
```

## peekaboo/commands/menubar.md

```yaml
summary: 'Work with macOS status items via peekaboo menubar'
read_when:
  - 'clicking Wi-Fi/Bluetooth/battery icons from automation flows'
  - 'enumerating third-party status items with indices for later use'
```

## peekaboo/commands/move.md

```yaml
summary: 'Position the cursor via peekaboo move'
read_when:
  - 'hovering elements without clicking'
  - 'lining up the pointer before a screenshot or drag sequence'
```

## peekaboo/commands/open.md

```yaml
summary: 'Open files/URLs with Peekaboo focus controls via peekaboo open'
read_when:
  - 'handing documents/URLs to specific apps from automation scripts'
  - 'needing structured output around macOS open events'
```

## peekaboo/commands/paste.md

```yaml
summary: 'Paste text or rich content via peekaboo paste'
read_when:
  - 'you want fewer steps than clipboard set + menu/hotkey paste + clipboard restore'
  - 'pasting rich text (RTF) into a targeted app/window without drift'
```

## peekaboo/commands/permissions.md

```yaml
summary: 'Check or explain required macOS permissions via peekaboo permissions'
read_when:
  - 'verifying screen recording + accessibility entitlements before a run'
  - 'needing grant instructions for CI or remote machines'
```

## peekaboo/commands/press.md

```yaml
summary: 'Send special keys or sequences via peekaboo press'
read_when:
  - 'navigating dialogs with arrow/tab/return patterns'
  - 'debugging scripted key sequences that need deterministic timing'
```

## peekaboo/commands/run.md

```yaml
summary: 'Execute .peekaboo.json scripts via peekaboo run'
read_when:
  - 'batching multiple CLI steps into a reusable automation script'
  - 'capturing structured execution results for regression tests'
```

## peekaboo/commands/scroll.md

```yaml
summary: 'Simulate mouse wheel movement via peekaboo scroll'
read_when:
  - 'panning long views or tables without dragging the scrollbar'
  - 'needing scroll telemetry (direction, ticks) for automation logs'
```

## peekaboo/commands/see.md

```yaml
summary: 'Capture annotated UI maps with peekaboo see'
read_when:
  - 'Collecting UI element IDs for automation'
  - 'Troubleshooting click/type targeting'
```

## peekaboo/commands/sleep.md

```yaml
summary: 'Insert millisecond delays via peekaboo sleep'
read_when:
  - 'throttling CLI scripts between UI actions'
  - 'forcing agents to wait for animations without adding custom loops'
```

## peekaboo/commands/space.md

```yaml
summary: 'Manage macOS Spaces via peekaboo space'
read_when:
  - 'switching desktops or moving windows for multi-space automation'
  - 'needing JSON snapshots of every Space and its windows'
```

## peekaboo/commands/swipe.md

```yaml
summary: 'Perform gesture-style drags via peekaboo swipe'
read_when:
  - 'animating trackpad-like swipes between coordinates or elements'
  - 'needing smooth, timed drags for carousels/cover flow UI'
```

## peekaboo/commands/tools.md

```yaml
summary: 'Inspect native tooling via peekaboo tools'
read_when:
  - 'deciding which automation tool to call from agents or scripts'
  - 'debugging missing tool registrations'
```

## peekaboo/commands/type.md

```yaml
summary: 'Inject keystrokes via peekaboo type'
read_when:
  - 'sending text or key chords into the focused element'
  - 'needing predictable focus + typing delays during UI automation'
```

## peekaboo/commands/visualizer.md

```yaml
summary: 'Exercise Peekaboo visual feedback animations via peekaboo visualizer'
read_when:
  - 'verifying Peekaboo.app overlay rendering'
  - 'debugging visualizer transport/animations'
```

## peekaboo/commands/window.md

```yaml
summary: 'Move, resize, and focus windows via peekaboo window'
read_when:
  - 'wrangling app windows before issuing UI interactions'
  - 'needing JSON receipts for close/minimize/maximize/focus actions'
```

## peekaboo/reports/pblog-guide.md

```yaml
summary: 'Review pblog - Peekaboo Log Viewer guidance'
read_when:
  - 'planning work related to pblog - peekaboo log viewer'
  - 'debugging or extending features described here'
```

## peekaboo/reports/playground-test-result.md

```yaml
summary: 'Review Peekaboo CLI Comprehensive Testing Report guidance'
read_when:
  - 'planning work related to peekaboo cli comprehensive testing report'
  - 'debugging or extending features described here'
```

## peekaboo/debug/menuitems.md

```yaml
summary: 'Menu bar item debug log for missing Trimmy status item on macOS 26.1'
read_when:
  - 'investigating missing menubar/status items'
  - 'debugging peekaboo menubar list output or CGS/AX heuristics'
```

## peekaboo/debug/visualizer-issues.md

```yaml
summary: 'Open issues for Peekaboo visualizer effects'
read_when:
  - 'verifying visual feedback coverage'
  - 'debugging missing visualizer animations'
```
