#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补 02_cpp 的「工程化与 SDK」子方向（20 道）。

为什么单独做：岗位偏好链里 SDK 开发排第一，Momenta 最高优先级岗位就是 C++ SDK。
但原题库 166 道 C++ 主要来自教学文档，偏语言基础，几乎不覆盖动态库 / ABI / 接口设计。

这些题的题述写得比较具体（场景 + 约束 + 问），因为 SDK 岗问的从来不是定义，
而是「你有约束时怎么选」。

用法: python tools/seed_cpp_sdk.py [--dry]
幂等：题卡带 sdk_seed 标记。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "02_cpp"
ID_BASE, SPAN = 600, 500
SUB = "工程化与 SDK"

ITEMS = [
    {
        "title": "动态库和静态库怎么选？你的部署场景会选哪个？",
        "diff": 2,
        "body": """## 题目

**场景**：你要给一个车载感知模块提供一个 C++ 库，下游有三个团队用，跑在同一个
SoC 上，整个系统有 200MB 的内存预算。交付形式要求「升级时不需要重新刷整个固件」。

**问**：动态库还是静态库？理由是什么？

## 口述答案

**要点**

- 这个场景选**动态库**。理由是「升级不刷整包」——动态库可以单独替换 `.so` 文件，静态库必须重新链接可执行文件。
- 静态库的优势是部署简单、没有运行时依赖、启动略快，代价是体积重复（三个团队各链一份就有三份代码）和升级成本高。
- 动态库的代价是**ABI 必须稳定**，一旦接口二进制不兼容，等于要重新联调所有下游。

**核心权衡**：要不要独立升级 → 要就动态库；能不能承受 ABI 维护成本 → 不能就静态库。

## 讲深一层

| 维度 | 静态库 `.a` | 动态库 `.so` |
|---|---|---|
| 链接时机 | 编译期，代码进可执行文件 | 运行期加载 |
| 体积 | 每个使用者一份 | 内存里共享一份 |
| 升级 | 必须重链 | 可单独替换（但要 ABI 兼容） |
| 依赖 | 无运行时依赖 | 依赖 libc / libstdc++ 版本 |
| 符号冲突 | 容易撞（全局符号都暴露） | 用 visibility 控制 |
| 加载速度 | 快 | 首次略慢（重定位） |

嵌入式场景还要额外看：是否允许 `dlopen`、文件系统是否只读、有没有签名校验。

## 高频追问

1. **动态库升级时怎么保证 ABI 兼容？** —— 只加不改，配合 soname 版本号；破坏性变更就升 major 版本，新旧共存。
2. **静态库会不会有符号重复定义？** —— 会。两个静态库都定义了同名全局符号就会冲突，动态库反而能靠符号可见性隔离。
3. **`-static-libstdc++` 是干什么的？** —— 把 libstdc++ 静态链进来，避免目标机版本太旧。代价是体积变大且不能用动态库里的类型跨边界。

## 易错点

- ❌ 「动态库一定更好，因为省内存」 —— 只有多进程共享时才省，单进程内没区别
- ❌ 忽略 libstdc++ 版本依赖 —— 目标机 GLIBCXX 版本低直接起不来
- ✅ 先问「升级方式」和「部署环境」，再谈技术优劣

## 关联项目

YOLO 推理部署（如果做过 `.so` 封装，直接讲这条链路）

## 来源

Linux 动态链接机制；`ld` / `ldd` 行为

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "动态库默认导出所有符号有什么问题？visibility 怎么设？",
        "diff": 3,
        "body": """## 题目

**场景**：你的 `.so` 里用了某个第三方库，静态链进去了。上线后发现主程序里另一个
模块调用同名函数时，调到了你的库里来。

**问**：为什么会这样？怎么保证只导出你想给外面用的那几个接口？

## 口述答案

**要点**

- 默认情况下 GCC 会把所有非 static 的全局符号导出，包括你静态链进来的第三方库的符号。两个 `.so` 有同名符号，谁先加载谁生效，这就是「符号抢占」。
- 解决办法是**默认隐藏 + 显式导出**：编译加 `-fvisibility=hidden`，把要暴露的接口用 `__attribute__((visibility("default")))` 或导出宏标出来。
- 好处不只是避免冲突：还能缩小 ABI 面（外部改不了你的内部实现）、加快加载（重定位的符号少了）、减小 `.so` 体积。

## 讲深一层

导出宏的典型写法：

```cpp
// export.h
#if defined(_WIN32)
#  define API_EXPORT __declspec(dllexport)
#  define API_IMPORT __declspec(dllimport)
#else
#  define API_EXPORT __attribute__((visibility("default")))
#  define API_IMPORT
#endif

#ifdef BUILDING_MYLIB
#  define MYLIB_API API_EXPORT
#else
#  define MYLIB_API API_IMPORT
#endif
```

验证导出面：

```bash
g++ -fvisibility=hidden -fPIC -shared -o libfoo.so *.cpp
nm -D --defined-only libfoo.so        # 只看动态符号表
readelf --dyn-syms libfoo.so | head
```

如果这里出现了一堆 `std::` 或第三方符号，说明第三方是静态链进来的且没隐藏。

## 高频追问

1. **为什么模板和内联函数不受 visibility 影响？** —— 它们在每个编译单元实例化，符号是弱符号（weak），隐藏要靠 `-fvisibility-inlines-hidden`。
2. **`static` 变量还需要 visibility 吗？** —— 不需要，`static` 本身就是内部链接。
3. **隐藏了还能被调试吗？** —— 能。`-g` 调试信息独立于符号表，用 addr2line / gdb 照样能看。

## 易错点

- ❌ 只加 `-fvisibility=hidden` 不加导出宏 —— 结果一个接口都导不出来，链接报 undefined
- ❌ 以为 `nm` 看不到就是没导出 —— 要看 `nm -D`（动态符号表）
- ❌ 在头文件里写 `__attribute__` 而不做平台宏 —— Windows 上编译不过

## 关联项目

YOLO 部署的 `.so` 封装

## 来源

GCC visibility 文档；ELF 符号表结构

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "给一个已发布的类加一个成员变量，会破坏 ABI 吗？",
        "diff": 3,
        "body": """## 题目

**场景**：你的 SDK 已经发给客户了，`class Session` 定义在头文件里。现在要给它加一个
`int retry_count_` 成员，只做内部记录，不加新接口。

**问**：客户需要重新编译吗？如果不重新编译会出什么问题？

## 口述答案

**要点**

- **会破坏 ABI**。加成员变量改变了 `sizeof(Session)` 和后续成员的偏移量。
- 如果客户代码里有 `Session s;`（栈上分配）或 `new Session`，而库内部按新大小操作，就会**越界写**或读写错位。
- 如果客户是通过指针/引用持有、且分配也发生在库内部，影响小一些——但仍然不保证，因为客户可能按旧布局访问公有成员。

**结论**：只要类的大小或布局变了，就必须重新编译客户端，除非用 pimpl 把实现细节藏到指针后面。

## 讲深一层

哪些改动破坏 ABI，哪些不破坏：

| 改动 | 破坏 ABI？ |
|---|---|
| 加非虚成员函数 | 否 |
| 加静态成员函数 | 否 |
| 加成员变量 | **是**（改 sizeof 和偏移） |
| 加虚函数 | **是**（改 vtable 布局，后面所有虚函数下标偏移） |
| 改函数返回类型 | 是 |
| 加默认参数 | 否（编译期展开） |
| 改 enum 值 | 是（如果值被内联进客户端） |
| 改内联函数实现 | 是（客户端用的是旧实现） |

## 高频追问

1. **怎么判断两个版本 ABI 是否兼容？** —— 有工具：`abi-compliance-checker`、`abi-dumper`，可以对比两个 `.so` 的符号和类型布局。
2. **加虚函数为什么后果更严重？** —— vtable 里虚函数按声明顺序排，插入一个会让后面所有虚函数的下标偏移，旧客户端调到错误的函数。
3. **能不能只在末尾加虚函数？** —— 实践上有争议：GCC 的 Itanium ABI 把虚函数按声明顺序放，末尾追加不改变已有下标，但会让 vtable 变长，仍然不保证跨编译器安全。**别依赖这个。**

## 易错点

- ❌ 「只是加个私有成员，外面看不见」 —— C++ 的私有成员仍然影响 sizeof 和布局
- ❌ 「客户用指针就没问题」 —— 客户可能在栈上构造、也可能按值传参
- ✅ 正确姿势：pimpl，或者干脆升 major 版本

## 关联项目

无

## 来源

Itanium C++ ABI；`abi-compliance-checker` 文档

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "pimpl 惯用法解决什么问题？代价是什么？",
        "diff": 2,
        "body": """## 题目

**场景**：你维护一个有 50 个源文件的 C++ 库，`Widget.h` 被 40 个文件 include。
现在要给 `Widget` 加一个私有成员，改完编译了 8 分钟。

**问**：怎么让私有成员的改动不再触发下游重编译？代价是什么？

## 口述答案

**要点**

- 用 **pimpl（pointer to implementation）**：头文件里只留一个 `std::unique_ptr<Impl>`，真正的成员定义在 `.cpp` 里。
- 这样改私有成员只重编一个 `.cpp`，下游 40 个文件不用动。同时它也是**保证 ABI 稳定**的手段——类的 sizeof 固定成一个指针大小。
- 代价：每次访问成员多一次指针间接跳转；构造函数要 `new`（一次堆分配）；析构要在 `.cpp` 里定义（否则 `unique_ptr` 的删除器在头文件里需要完整类型）。

## 讲深一层

```cpp
// Widget.h
class Widget {
public:
    Widget();
    ~Widget();                      // 必须声明，定义放 cpp
    Widget(Widget&&) noexcept;
    Widget& operator=(Widget&&) noexcept;
    void draw() const;
private:
    struct Impl;                    // 只声明
    std::unique_ptr<Impl> p_;       // sizeof = 8（64 位）
};
```

```cpp
// Widget.cpp
struct Widget::Impl { /* 真正的成员，可以随便改 */ };
Widget::Widget() : p_(std::make_unique<Impl>()) {}
Widget::~Widget() = default;        // 必须在这里，Impl 完整
```

## 高频追问

1. **为什么析构函数必须在 cpp 里定义？** —— `unique_ptr<Impl>` 析构需要 `Impl` 完整类型；头文件里 `Impl` 只有声明，默认析构会触发 `static_assert` 失败。
2. **能不能用 `shared_ptr` 省掉析构定义？** —— 能。`shared_ptr` 的类型擦除让析构可以在实例化点生成，代价是多一个控制块。
3. **pimpl 和「编译防火墙」是一回事吗？** —— 是同一件事的两种叫法。Firefox 里叫 compiler firewall，标准里叫 opaque pointer。
4. **多一次跳转会明显变慢吗？** —— 热路径上会有影响（多一次 cache 访问）。可以把最热的方法做成非 pimpl，或者用 `-flto` 让它内联。

## 易错点

- ❌ 头文件里直接写 `~Widget() = default;` —— 编译报错「incomplete type」
- ❌ 忘了实现移动构造 —— `unique_ptr` 不可拷贝，默认拷贝构造会被删除，容易编译失败
- ❌ 对每个小类都用 pimpl —— 过度设计，只有被大量 include 的公共头才值得

## 关联项目

无

## 来源

C++ 惯用法（Herb Sutter, *Exceptional C++*）

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "改一行注释为什么触发全量重编译？怎么阻断？",
        "diff": 2,
        "body": """## 题目

**场景**：你在 `common.h` 里改了一句注释，结果整个工程 300 个文件重编译，跑了 15 分钟。

**问**：构建系统为什么这么判？怎么减少这种连带重编译？

## 口述答案

**要点**

- Make / Ninja 的依赖判定是**基于时间戳的文件级**判断：头文件变了 → 所有 include 它的源文件都算脏。它不知道你改的是注释还是代码。
- 阻断手段有三层：**减少 include 数量**（前置声明、pimpl）、**减少热点头文件的变更频率**（把稳定的东西放公共头，易变的东西下沉）、**用 ccache / 分布式编译**兜底。
- 最根本的是降低头文件的耦合度：一个头文件被 300 个文件 include，本身就是设计问题。

## 讲深一层

具体手段按收益排序：

| 手段 | 效果 | 代价 |
|---|---|---|
| 前置声明替代 include | 直接减少依赖边 | 只能在不需要完整类型时用 |
| pimpl 隐藏私有成员 | 私有改动零传播 | 一次间接跳转 |
| 抽出稳定接口头 | 热点头变更变少 | 需要设计分层 |
| `ccache` / `sccache` | 命中缓存时近乎免费 | 首次无收益，需要配置 |
| 预编译头（PCH） | 减少解析时间 | 增加构建复杂度，容易失效 |

注意：`ccache` 对「注释改动」特别有效——预处理后的内容相同，hash 相同，直接命中。

## 高频追问

1. **能不能让构建系统忽略注释改动？** —— 有些工具（如 `ccache` 的 direct mode）能通过预处理器输出判断，但 Make 本身做不到。
2. **`#pragma once` 和 include guard 有性能差别吗？** —— 现代编译器里 `#pragma once` 略快（不用打开文件比对宏），但不标准。
3. **模块（C++20 modules）能解决吗？** —— 能，它是编译期的语义级依赖，不是文件级。但工程落地还不成熟。

## 易错点

- ❌ 用「把 include 挪到 cpp 里」解决一切 —— 只在不需要完整类型时有效
- ❌ 依赖 PCH 却没配好依赖 —— 改了头文件 PCH 不重建，出现诡异的不一致
- ✅ 先量化：用 `-ftime-trace` 或构建系统的统计看时间花在哪

## 关联项目

C++ 工程化开发

## 来源

Make/Ninja 依赖模型；`ccache` 直接模式

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "undefined symbol 报错，排查顺序是什么？",
        "diff": 2,
        "body": """## 题目

**场景**：程序启动时报
`error while loading shared libraries: libfoo.so: undefined symbol: _ZN3foo3Bar4initEv`

**问**：这个符号是什么？按什么顺序排查？

## 口述答案

**要点**

- `_ZN3foo3Bar4initEv` 是 **C++ 名字修饰（mangling）**后的符号，解出来是 `foo::Bar::init()`。
- 排查顺序：① `c++filt` 解符号 → ② `nm -D` 看提供方有没有导出这个符号 → ③ 检查库有没有被真正链接（`ldd`）→ ④ 检查链接顺序和 `--as-needed` → ⑤ 检查是不是 C/C++ 混用缺 `extern "C"`。

## 讲深一层

```bash
c++filt _ZN3foo3Bar4initEv          # → foo::Bar::init()
nm -D --defined-only libfoo.so | grep Bar4init   # 提供方有没有
ldd ./app | grep foo                # 运行时依赖有没有
readelf -d ./app | grep NEEDED      # 编译期记录的依赖
```

常见原因对照：

| 现象 | 原因 |
|---|---|
| 编译期就报 undefined reference | 链接时漏了 `-lfoo`，或顺序不对 |
| 链接过但运行时 undefined symbol | `.so` 本身缺依赖，或符号被 visibility 隐藏 |
| 只有 C 调用 C++ 时报错 | 缺 `extern "C"`，符号名带了 C++ 修饰 |
| 换编译器后报错 | libstdc++ 版本不匹配（`GLIBCXX_3.4.29` not found） |

## 高频追问

1. **`-Wl,--no-undefined` 有什么用？** —— 让链接器在构建期就检查未定义符号，把运行时的坑提前到编译期。做 SDK 建议开。
2. **`--as-needed` 为什么会「吃掉」库？** —— 链接器发现当前目标没用到该库的符号就不记录依赖，导致运行时缺。经典坑，调换顺序或加 `--no-as-needed`。
3. **静态库的符号找不到怎么办？** —— 静态库按需提取，被依赖的库要放后面；循环依赖用 `-Wl,--start-group ... -Wl,--end-group`。

## 易错点

- ❌ 看到修饰名就直接猜 —— 用 `c++filt` 解，别硬读
- ❌ 只看 `nm` 不看 `nm -D` —— 内部符号和动态符号是两回事
- ❌ 加 `-lfoo` 放最前面 —— 静态库场景下会失效

## 关联项目

YOLO 部署（链接推理库时的实际报错）

## 来源

`ld` 手册；Itanium 名字修饰规则

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "为什么不该让异常穿过动态库边界？",
        "diff": 3,
        "body": """## 题目

**场景**：你的 SDK 内部大量用异常做错误处理。客户用另一个编译器版本编译，
在你抛异常的地方直接崩了，报 `terminate called after throwing an instance of ...`。

**问**：为什么？SDK 边界该怎么处理错误？

## 口述答案

**要点**

- 异常跨越 ABI 边界依赖**两侧使用兼容的异常实现**（Itanium ABI 的 unwind 表、异常类布局、`type_info` 比较方式）。不同编译器/版本/标准库之间不保证兼容。
- 崩溃的直接原因通常是：异常在库 A 抛出，栈展开到库 B 时找不到对应的 catch，或者 `type_info` 不相等导致没匹配上，最终 `std::terminate`。
- 正确做法：**SDK 边界不抛异常**。内部随便用，出边界前统一转成错误码或返回值，并给所有导出函数标 `noexcept`。

## 讲深一层

边界转换的写法：

```cpp
// 内部：用异常
void LoadImpl() { if (bad) throw std::runtime_error("..."); }

// 边界：转错误码，标 noexcept
MYLIB_API int Load() noexcept {
    try {
        LoadImpl();
        return 0;
    } catch (const std::bad_alloc&) { return -1; }
    catch (const std::exception&)   { return -2; }
    catch (...)                     { return -3; }   // 兜底，防漏网
}
```

为什么要 `catch (...)`：漏网的异常一旦越过 `noexcept` 边界，`std::terminate` 立即调用，连日志都来不及打。

## 高频追问

1. **`noexcept` 能阻止异常逃逸吗？** —— 不能阻止抛出，但会在边界处调 `std::terminate`。它是个「契约检查」，不是安全网。
2. **同一编译器不同版本呢？** —— 通常兼容（Itanium ABI 稳定），但标准库实现变了（比如 libstdc++ 的 `std::string` SSO 改动）仍可能出问题。
3. **C 接口怎么处理错误？** —— 纯 C 无法用异常，只能返回值 + 错误信息查询函数（如 `GetLastError()`）。Windows API 就是这套。

## 易错点

- ❌ 只在文档里写「本接口可能抛异常」 —— 客户端编译器不兼容时照样崩
- ❌ `catch (...)` 里吞掉所有错误不记录 —— 排查时没有信息
- ✅ 导出函数一律 `noexcept`，返回值给错误码，另配一个拿错误详情的函数

## 关联项目

无

## 来源

Itanium C++ ABI 异常处理；`std::terminate` 语义

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "跨编译器传 std::string 有什么风险？SDK 接口该用什么类型？",
        "diff": 3,
        "body": """## 题目

**场景**：你的 SDK 接口写成 `void SetName(std::string name)`。客户用 GCC 9 编译，
你用 GCC 11 编译的库。客户传进来一个长字符串，你的库里读出来是乱码。

**问**：为什么？接口参数该用什么类型？

## 口述答案

**要点**

- `std::string` 的**内存布局是实现细节**。GCC 9 和 GCC 11 的 libstdc++ 用了不同版本的 SSO（小字符串优化）策略，`std::string` 的 sizeof 和内部指针位置可能不同。
- 短字符串（存在对象内部）没问题，超过 SSO 阈值（通常 15 字节）就走堆，布局差异暴露，读出来是垃圾。
- 正确做法：**边界只传 C 风格的数据 + 长度**，或用自己的 POD 结构。
  `void SetName(const char* name, size_t len)` 或者封装成 `struct MyStr { const char* p; size_t n; }`。

## 讲深一层

为什么 `const char*` 安全：它就是个指针，所有编译器表示一致。长度单独传，避免依赖 `strlen`（也避免中间有 `\\0` 时截断）。

C++17 起有更好的选择：`std::string_view`——但它**同样有布局问题**，只能在同一套工具链内部用，跨 ABI 边界还是不行。

| 类型 | 跨 ABI 安全 | 说明 |
|---|---|---|
| `const char*` + `len` | ✅ | 最稳，纯 C |
| `std::string_view` | ⚠️ | 布局是两个指针/长度，标准未规定顺序 |
| `std::string` | ❌ | SSO 实现相关 |
| `std::vector<T>` | ❌ | 三个指针的顺序未规定 |
| POD 结构体 | ✅ | 需固定对齐和大小 |

## 高频追问

1. **那返回值怎么返回字符串？** —— 两种：调用方传缓冲区（`int GetName(char* buf, size_t cap)`），或库分配 + 提供 `Free` 函数。前者更安全。
2. **`extern "C"` 能解决吗？** —— 解决的是名字修饰，不解决类型布局。用了 `extern "C"` 但参数还是 `std::string` 照样崩。
3. **为什么 MSVC 和 GCC 之间更严重？** —— 连 ABI 规范都不同（MSVC 有自己的 ABI），差异更大。

## 易错点

- ❌ 只在同工具链测过就认为没问题 —— 客户可能用别的编译器
- ❌ 用 `std::string` 但只在文档写「需同版本编译器」 —— 客户不会看
- ✅ 定接口前先问「客户端用什么工具链」

## 关联项目

无

## 来源

libstdc++ SSO 实现；C++ 标准对容器布局不作规定

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "extern \"C\" 解决什么问题？为什么它不能有重载？",
        "diff": 2,
        "body": """## 题目

**场景**：你要让一个 C 程序调用你的 C++ 库，直接在头文件里声明了函数，
链接时报 `undefined reference to 'init'`，但你的库里明明有 `init` 函数。

**问**：原因是什么？`extern "C"` 做了什么？为什么它下面不能写重载？

## 口述答案

**要点**

- 原因是 **C++ 名字修饰**。C++ 编译器会把 `init` 编成 `_Z4initv` 这样的符号，而 C 编译器找的是 `init`，两边对不上。
- `extern "C"` 的作用是**禁止名字修饰**，让符号名保持原样。它只影响链接名，不影响调用约定和类型检查。
- 不能有重载是因为重载依赖修饰后的不同符号名来区分；禁用修饰后，两个 `init(int)` 和 `init(double)` 会生成同一个符号 `init`，链接冲突。

## 讲深一层

典型写法（头文件要能被 C 和 C++ 同时 include）：

```cpp
#ifdef __cplusplus
extern "C" {
#endif

int  mylib_init(void);
void mylib_free(void* p);

#ifdef __cplusplus
}
#endif
```

注意 `extern "C"` 只对**函数**和**函数指针**有效，对类成员函数不能直接用（成员函数隐含 `this`，且依赖类布局）。

## 高频追问

1. **`extern "C"` 会改变调用约定吗？** —— 不会。它只改符号名。调用约定是 `__cdecl` / `__stdcall` 这类，Windows 上要单独指定。
2. **C++ 里能调 C 的库吗？** —— 能，同样用 `extern "C"` 声明，否则会去找修饰后的名字。
3. **`extern "C++"` 存在吗？** —— 存在，用于在 `extern "C"` 块里恢复 C++ 链接，很少用。

## 易错点

- ❌ 只在 .cpp 里写 `extern "C"` 而不改头文件 —— 客户端编译时仍按 C++ 修饰
- ❌ 用 `extern "C"` 包住模板或类 —— 语法上不允许
- ✅ 头文件一定要加 `#ifdef __cplusplus` 双保险

## 关联项目

无

## 来源

C++ 标准 [dcl.link]；Itanium 名字修饰

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "CMake 里 PUBLIC、PRIVATE、INTERFACE 到底区别在哪？",
        "diff": 2,
        "body": """## 题目

**场景**：你写了一个库 target，用了 OpenCV 和 Eigen。OpenCV 只在 .cpp 里用，
Eigen 出现在头文件里（因为公有接口有 `Eigen::Matrix` 参数）。

**问**：这两个依赖该用 PUBLIC、PRIVATE 还是 INTERFACE 声明？

## 口述答案

**要点**

- **OpenCV → PRIVATE**：只在实现里用，下游不需要知道。它的 include 路径和链接库不会传给下游。
- **Eigen → PUBLIC**（或 INTERFACE）：它出现在公有头文件里，下游编译时必须能找到 Eigen 的头文件，否则编译失败。
- 记忆口诀：**PRIVATE 给自己用，INTERFACE 给别人用，PUBLIC 是两者都要。**

## 讲深一层

```cmake
add_library(mylib src/a.cpp)

target_link_libraries(mylib
    PRIVATE  opencv_core          # 只是实现里用
    PUBLIC   Eigen3::Eigen        # 头文件里出现，下游也要
)

# 纯头文件库（没有 .cpp）
add_library(header_only INTERFACE)
target_include_directories(header_only INTERFACE include/)
target_link_libraries(header_only INTERFACE Eigen3::Eigen)
```

三个关键字实际控制的东西一样，只是**传播方向**不同：

| | 作用于自己 | 传给下游 |
|---|---|---|
| PRIVATE | ✅ | ❌ |
| INTERFACE | ❌ | ✅ |
| PUBLIC | ✅ | ✅ |

`target_include_directories`、`target_compile_definitions`、`target_compile_options` 都遵循同一套规则。

## 高频追问

1. **用错了会怎样？** —— OpenCV 写成 PUBLIC：下游被传染一堆不需要的 include 路径，编译变慢，还可能符号冲突。Eigen 写成 PRIVATE：下游编译直接找不到 `Eigen::Matrix`。
2. **`INTERFACE` 用在普通库上会怎样？** —— 语法允许但没意义：库自己不编译，只向下游传递。
3. **`LINK_LIBRARIES` 和 `LINK_PUBLIC` 是什么？** —— 老式写法（CMake 2.8 时代），等价于 PUBLIC，已废弃，别再用。

## 易错点

- ❌ 全部写 PUBLIC「反正能编过」 —— 依赖泄漏，下游构建时间暴涨
- ❌ 用全局 `include_directories()` 而不是 target 级别 —— 作用域失控，无法导出
- ✅ 判断标准只有一个：**这个东西是否出现在公有头文件里**

## 关联项目

C++ 工程化开发

## 来源

CMake 官方 `target_link_libraries` 文档

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "为什么 SDK 必须写 install 和 export？不写会怎样？",
        "diff": 3,
        "body": """## 题目

**场景**：你的库编译通过了，客户拿到源码后要手动改 include 路径、手动写 `-L -l`。
你觉得这样也行，但客户抱怨「不知道怎么接」。

**问**：`install` 和 `export` 是干什么的？不写有什么后果？

## 口述答案

**要点**

- `install` 决定「装什么、装到哪」：头文件、`.so`、CMake 配置文件。
- `export` 生成 `xxxConfig.cmake` 和 `xxxConfigVersion.cmake`，让下游能直接 `find_package(xxx)`，自动拿到 include 路径、链接库、编译选项。
- 不写的话，下游只能靠文档猜路径——这等于把集成成本转嫁给客户，SDK 的可用性大打折扣。

## 讲深一层

最小可用的 install/export：

```cmake
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

install(TARGETS mylib EXPORT mylibTargets
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(EXPORT mylibTargets
        FILE mylibTargets.cmake
        NAMESPACE mylib::
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/mylib)

write_basic_package_version_file(
    mylibConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/mylibConfigVersion.cmake
              cmake/mylibConfig.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/mylib)
```

下游使用：

```cmake
find_package(mylib 1.2 REQUIRED)
target_link_libraries(app PRIVATE mylib::mylib)
```

`COMPATIBILITY SameMajorVersion` 表示 1.x 之间可替换、2.0 不兼容——这和 soname 的语义要对齐。

## 高频追问

1. **`mylibConfig.cmake` 里要写什么？** —— 通常只需要 `include(mylibTargets.cmake)`，加上依赖的 `find_dependency()`。
2. **`NAMESPACE` 有什么用？** —— 防止 target 名冲突。加 `mylib::` 前缀后，下游不会和别人的 `mylib` target 撞。
3. **Windows 上有什么额外要求？** —— 导出 `.lib`（导入库）+ `.dll`，还要处理 `__declspec(dllimport)`。

## 易错点

- ❌ 只 `install(TARGETS)` 不 `install(EXPORT)` —— 文件装了但下游 `find_package` 找不到
- ❌ 漏了版本文件 —— `find_package(mylib 1.2)` 直接失败
- ✅ 写完自己建个空工程 `find_package` 验证一遍

## 关联项目

C++ 工程化开发

## 来源

CMake `install(EXPORT)` / `CMakePackageConfigHelpers` 文档

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "soname 是什么？版本号怎么映射到文件名？",
        "diff": 3,
        "body": """## 题目

**场景**：你发布了一个动态库，目录里有三个文件：
`libfoo.so`、`libfoo.so.1`、`libfoo.so.1.2.3`。

**问**：这三个分别是什么？为什么需要三个？升级时改哪个？

## 口述答案

**要点**

- `libfoo.so.1.2.3` 是**真实文件**（major.minor.patch）。
- `libfoo.so.1` 是 **soname**（符号链接），程序运行时找的是它。它只含 major 号。
- `libfoo.so` 是**开发链接名**（另一个符号链接），编译时 `-lfoo` 找的是它。
- 这么设计是为了让「小版本升级」不影响已编译的程序：1.2.3 → 1.2.4 只换真实文件，soname 不变，程序无需重编。

## 讲深一层

编译时的关键参数：

```bash
g++ -shared -fPIC -o libfoo.so.1.2.3 *.cpp \\
    -Wl,-soname,libfoo.so.1
```

`-soname` 会把 `libfoo.so.1` 写进 `.so` 的 `DT_SONAME` 字段。程序链接时，链接器把 soname 记进可执行文件的 `DT_NEEDED`，运行时动态加载器就按这个名字找。

查看：

```bash
readelf -d libfoo.so.1.2.3 | grep SONAME
readelf -d ./app | grep NEEDED
```

版本升级策略：

| 改动类型 | 版本位 | soname 变吗 | 下游要重编吗 |
|---|---|---|---|
| 修 bug、内部优化 | patch | 否 | 否 |
| 加新接口（兼容） | minor | 否 | 否（想用新接口才重编） |
| 破坏 ABI | major | **是** | 是 |

## 高频追问

1. **不写 `-soname` 会怎样？** —— 链接器用文件名当 soname，即 `libfoo.so.1.2.3`，运行时按这个全名找。升级小版本就找不到，必须重建符号链接。
2. **`ldconfig` 干的是什么？** —— 扫描库目录，重建 `/etc/ld.so.cache`，让动态加载器能快速按 soname 找到文件。
3. **为什么 major 变了要并存？** —— 让新旧程序各用各的，不用同时升级所有依赖。

## 易错点

- ❌ 三个文件都做成真实文件 —— 升级时忘改其中一个，程序起不来
- ❌ 破坏 ABI 却只升 minor —— 下游不重编就崩
- ❌ 忘了跑 `ldconfig` —— 装完库程序仍找不到

## 关联项目

无

## 来源

`ld.so` 手册；`elf(5)` 的 `DT_SONAME` / `DT_NEEDED`

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "接口用纯虚基类还是回调函数？各有什么坑？",
        "diff": 3,
        "body": """## 题目

**场景**：你的 SDK 需要让客户在「检测到目标」时收到通知。有两种设计：
A. 定义 `class Listener { virtual void OnDetect(const Result&) = 0; }`，客户继承；
B. 提供 `SetCallback(void(*)(const Result*, void*), void* user)`。

**问**：选哪个？各自的代价是什么？

## 口述答案

**要点**

- **只有一两个回调点 → 选回调**（B）。简单、无 vtable 依赖、跨语言友好。
- **需要一组相关方法、有状态、要做生命周期管理 → 选纯虚基类**（A）。接口更清晰，但引入 vtable 布局依赖。
- 纯虚基类的坑：**vtable 布局是 ABI 的一部分**，你在基类里加一个虚函数，客户编译的旧代码可能调到错误的槽位。

## 讲深一层

对比：

| 维度 | 纯虚基类 | 回调函数 |
|---|---|---|
| 扩展点数量 | 多方法自然 | 每个点一个 setter |
| 跨语言 | 难（要适配） | 易（C 函数指针） |
| ABI 风险 | 高（vtable 布局） | 低（函数指针大小固定） |
| 生命周期 | 要约定谁持有、何时析构 | `user` 指针自己管 |
| 状态 | 天然有（this） | 靠 `void* user` |
| 异常安全 | 客户实现可能抛 | 同样要防，但更容易包住 |

混合方案：用纯虚基类，但**只在末尾追加虚函数**（不推荐依赖这个），或者干脆用 `struct` 存函数指针表（COM 风格）。

## 高频追问

1. **虚基类的析构为什么必须是 virtual？** —— 通过基类指针删除派生对象时，非虚析构只调基类析构，派生部分泄漏。
2. **能不能让客户实现里抛异常？** —— 不能，必须在你调用它的地方包 `try/catch`，否则异常穿出你的 ABI 边界。
3. **COM 为什么用函数指针表？** —— 为了跨编译器、跨语言（C 也能用），且 vtable 布局由接口定义固定，不受编译器影响。

## 易错点

- ❌ 基类析构不是 virtual —— 内存泄漏
- ❌ 在基类中间插入虚函数 —— 破坏已发布的 ABI
- ❌ 回调里 `user` 指针生命周期没约定 —— 悬空指针崩溃

## 关联项目

无

## 来源

Itanium C++ ABI vtable 布局；COM 接口设计

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "单例放在动态库里，为什么会出现两个实例？",
        "diff": 3,
        "body": """## 题目

**场景**：你在头文件里写了一个 `Singleton::instance()`，返回函数内静态对象。
主程序和两个插件都 include 了这个头文件。调试时发现三个模块拿到的不是同一个对象。

**问**：为什么？怎么修？

## 口述答案

**要点**

- 函数内静态变量（Meyers singleton）的实例化点在**每个编译单元**里。头文件被三个模块 include，就可能在三个模块里各生成一份（取决于内联和符号可见性）。
- 动态库里更是如此：每个 `.so` 有自己的数据段，未导出的弱符号各有一份。
- 修法：**把单例的定义移到某个 `.cpp` 里**，只留声明在头文件，并确保符号被导出（或用 `-fvisibility` 显式导出）。

## 讲深一层

```cpp
// 错误：头文件里
class Config {
public:
    static Config& instance() {
        static Config c;     // 每个 TU 一份
        return c;
    }
};

// 正确：头文件只声明
class MYLIB_API Config {
public:
    static Config& instance();   // 无定义
};

// .cpp 里
Config& Config::instance() {
    static Config c;             // 全库唯一
    return c;
}
```

另一个陷阱：**跨 `.so` 的全局对象初始化顺序**。不同 `.so` 的静态初始化顺序未定义，如果 A 的构造函数依赖 B 的单例，可能拿到未初始化的对象。

## 高频追问

1. **`-fvisibility=hidden` 会让单例分裂吗？** —— 不会，反而更明确：不导出的符号本来就该每个库一份。
2. **怎么保证跨库唯一？** —— 必须显式导出，或者把实例放到一个明确的基础库里，其他库链接它。
3. **静态初始化顺序问题怎么破？** —— 用「首次使用时初始化」（Meyers singleton 本身就是这个思路），或者干脆不用全局对象。

## 易错点

- ❌ 头文件里直接定义 `static` 成员并初始化 —— C++17 的 inline 变量能解决，但跨 `.so` 仍不保证
- ❌ 在析构函数里依赖别的全局对象 —— 析构顺序反着来，可能已销毁
- ✅ 单例定义放 `.cpp`，接口导出，这是唯一可靠做法

## 关联项目

无

## 来源

C++ 静态存储期初始化规则；ELF 数据段隔离

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "怎么给已发布的 SDK 做一次不破坏兼容性的接口升级？",
        "diff": 3,
        "body": """## 题目

**场景**：你的 SDK v1.2 已发布，接口里有个 `Detect(const Image&, Result*)`。
现在需要支持「只检测某一类目标」，要加一个类别过滤参数。

**问**：怎么加才不让现有客户重编译？

## 口述答案

**要点**

- **不要改老函数签名**。改签名 = 改符号名 = 老客户链接不上。
- 做法：**新增一个函数**，老的保留并转调新的。
  `DetectV2(const Image&, const DetectOptions*, Result*)`，老 `Detect` 内部构造默认 options 调 V2。
- 用**扩展结构体**而不是加参数：`struct DetectOptions { uint32_t size; /* 后续版本在末尾加字段 */ }`，客户传 `sizeof` 便于库内做版本兼容。

## 讲深一层

扩展结构体的标准套路（Windows API 常用）：

```cpp
struct DetectOptions {
    uint32_t struct_size;     // = sizeof(DetectOptions)，调用方填
    uint32_t class_filter;    // v1.2 新增
    // 未来版本继续在末尾加，老客户传旧 sizeof，库内按 size 判断字段是否存在
};
```

库内：

```cpp
if (opt && opt->struct_size >= offsetof(DetectOptions, class_filter) + sizeof(uint32_t)) {
    use_filter = opt->class_filter;
}
```

这套做法的好处：**新老客户端共存于同一个库**，且不需要升 major。

## 高频追问

1. **为什么不直接加默认参数？** —— 默认参数是编译期展开，客户不重编就还是老调用，行为不符合预期；而且它不改变符号名，看起来「兼容」了但语义没升级。
2. **要废弃老接口怎么办？** —— 先标记 `[[deprecated]]`，保留至少一个大版本，文档写清迁移路径，再在 major 版本删除。
3. **结构体扩展会破坏 ABI 吗？** —— 只要新字段加在**末尾**且调用方按 `sizeof` 传，不破坏；加在中间就破坏了。

## 易错点

- ❌ 直接改函数签名 —— 老客户的二进制链接不上
- ❌ 结构体字段插在中间 —— 老客户按旧偏移读，读到错位数据
- ❌ 用 `bool` 当新参数类型 —— 大小和对齐在不同 ABI 下可能不同，用 `uint32_t`

## 关联项目

无

## 来源

Win32 API 结构体版本化惯例；ABI 兼容规则

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "dlopen 和 dlsym 怎么用？有哪些坑？",
        "diff": 2,
        "body": """## 题目

**场景**：你要做一个插件机制，主程序启动时扫描目录下的 `.so` 并加载，
每个插件导出一个 `create_plugin()` 函数。

**问**：怎么实现？有哪些必须处理的边界？

## 口述答案

**要点**

- 用 `dlopen(path, RTLD_LAZY)` 加载，`dlsym(handle, "create_plugin")` 取函数指针，
  用完 `dlclose` 卸载。
- 三个必须处理：**每次都查 `dlerror()`**（`dlsym` 可能合法返回 NULL）、**符号名要 `extern "C"`**、**卸载前保证没有悬空指针**。

## 讲深一层

```cpp
#include <dlfcn.h>

using CreateFn = Plugin* (*)();

Plugin* LoadPlugin(const char* path) {
    void* h = dlopen(path, RTLD_NOW | RTLD_LOCAL);
    if (!h) { fprintf(stderr, "dlopen: %s\\n", dlerror()); return nullptr; }

    dlerror();                              // 清空错误状态
    auto fn = reinterpret_cast<CreateFn>(dlsym(h, "create_plugin"));
    const char* err = dlerror();
    if (err) { fprintf(stderr, "dlsym: %s\\n", err); dlclose(h); return nullptr; }

    return fn();
}
```

`RTLD_LAZY` 是延迟解析（调用时才找符号），`RTLD_NOW` 是立即解析（加载时全找，出错早发现）。
**插件系统建议用 `RTLD_NOW`**，别把错误拖到运行时。

`RTLD_LOCAL`（默认）让符号只对本库可见，`RTLD_GLOBAL` 会把符号加入全局表影响其他库。

## 高频追问

1. **`dlsym` 返回 NULL 一定是失败吗？** —— 不一定，符号值本身可能就是 NULL。所以要先 `dlerror()` 清空，调用后再查一次。
2. **卸载后原来的对象还能用吗？** —— 不能。`dlclose` 之后库代码被卸载，任何指向它内部函数的指针、任何该库分配的对象都失效。
3. **插件之间互相依赖怎么办？** —— 用 `RTLD_GLOBAL` 让先加载的符号可见，但要小心符号冲突；更稳的是插件只依赖主程序暴露的接口。

## 易错点

- ❌ 不检查 `dlopen` 返回 NULL —— 段错误
- ❌ `dlsym` 后不查 `dlerror` —— 拿空指针调用，崩
- ❌ 忘记 `extern "C"` —— 导出符号名被修饰，`dlsym` 找不到
- ❌ 卸载顺序错 —— 插件还活着就把库卸了

## 关联项目

无

## 来源

`dlopen(3)` man page

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "find_package 找不到库，按什么顺序排查？",
        "diff": 2,
        "body": """## 题目

**场景**：`CMakeLists.txt` 里写了 `find_package(OpenCV REQUIRED)`，
报 `Could not find a package configuration file provided by "OpenCV"`。
但 `pkg-config --modversion opencv4` 能正常输出。

**问**：为什么会这样？排查顺序是什么？

## 口述答案

**要点**

- `find_package` 有两套模式：**Config 模式**（找 `OpenCVConfig.cmake`）和 **Module 模式**（找 `FindOpenCV.cmake`）。报错信息说找不到 config 文件，说明进了 Config 模式但没找到。
- 排查顺序：① 库到底装在哪（`pkg-config --variable=prefix`）→ ② 该目录下有没有 `*Config.cmake` → ③ `CMAKE_PREFIX_PATH` 有没有指过去 → ④ 大小写和组件名对不对。

## 讲深一层

```bash
pkg-config --variable=prefix opencv4     # → /usr/local
find /usr/local -name "OpenCVConfig.cmake" 2>/dev/null
```

有的话：

```cmake
set(CMAKE_PREFIX_PATH "/usr/local" ${CMAKE_PREFIX_PATH})
find_package(OpenCV REQUIRED COMPONENTS core imgproc)
```

没有 config 文件时，退一步用 Module 模式或手动指定：

```cmake
# 让 CMake 先试 MODULE 再试 CONFIG
find_package(OpenCV REQUIRED MODULE)
```

排查对照表：

| 现象 | 原因 |
|---|---|
| 报找不到 config 文件 | 库是源码编译的但没 `make install`，或装到了非标准路径 |
| 找到了但链接报错 | 版本不匹配，或组件名写错（`opencv4` vs `OpenCV`） |
| `pkg-config` 有但 CMake 没有 | pkg-config 走的是 `.pc` 文件，CMake 走的是 `Config.cmake`，两套独立 |

## 高频追问

1. **`CMAKE_PREFIX_PATH` 和 `OpenCV_DIR` 有什么区别？** —— 前者是搜索根目录列表，后者直接指定某个包的 config 所在目录，优先级更高。
2. **交叉编译时要注意什么？** —— 要设 `CMAKE_FIND_ROOT_PATH` 和 `CMAKE_SYSROOT`，否则会找到主机的库。
3. **`REQUIRED` 去掉能自动降级吗？** —— 能，`find_package(X)` 找不到时 `X_FOUND` 为假，可以用 `if(X_FOUND)` 分支处理可选依赖。

## 易错点

- ❌ 只改 `PKG_CONFIG_PATH` 以为 CMake 会跟着变 —— 两套机制无关
- ❌ 装到 `/usr/local` 但没设 `CMAKE_PREFIX_PATH` —— CMake 默认不搜这里
- ✅ 用 `cmake --debug-find` 看它到底搜了哪些路径

## 关联项目

C++ 工程化开发（YOLO 部署时链接 OpenCV）

## 来源

CMake `find_package` 文档；`pkg-config` 机制

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "两个静态库互相依赖，链接为什么会失败？",
        "diff": 2,
        "body": """## 题目

**场景**：`liba.a` 里的函数调用了 `libb.a` 的函数，`libb.a` 又反过来调用 `liba.a`。
你写 `-la -lb` 链接失败，写 `-lb -la` 也失败。

**问**：为什么？怎么解？

## 口述答案

**要点**

- 链接器处理静态库是**单趟从左到右扫描**的：遇到 `liba.a` 时，只把「当前已产生未定义符号」对应的目标文件抽出来。此时还没有未定义符号指向 `libb` 的内容，所以 `libb.a` 里的东西不会被抽。
- 循环依赖时，无论什么顺序，总有一边的符号在后面才出现，扫过去就补不上了。
- 解法：**用 `--start-group` / `--end-group` 让链接器反复扫描**，或者把两个库合并成一个。

## 讲深一层

```bash
# 循环依赖的标准解法
g++ main.o -Wl,--start-group -la -lb -Wl,--end-group -o app
```

三个层次的理解：

| 情况 | 顺序 | 结果 |
|---|---|---|
| a 依赖 b，无循环 | `-la -lb` ✅ | b 放后面，正确 |
| a 依赖 b，无循环 | `-lb -la` ❌ | 先扫 b 时没需求，被跳过 |
| 循环依赖 | 任意顺序 ❌ | 必须 `--start-group` |

根本上，静态库的符号解析是**需求驱动**的：只有当前存在未定义符号，才会去库里的成员对象中找。

## 高频追问

1. **`--start-group` 的代价是什么？** —— 链接器要在组内反复迭代直到没有新符号，大库多时链接变慢。
2. **动态库有这个问题吗？** —— 没有，动态库是运行时解析，不受顺序影响（但 `--as-needed` 会带来另一种坑）。
3. **怎么从根上避免？** —— 拆掉循环依赖。两个库互相引用通常说明边界划错了，把公共部分抽成第三个库。

## 易错点

- ❌ 反复调换 `-l` 顺序试图碰运气 —— 循环依赖下不可能成功
- ❌ 把 `-l` 放在 `.o` 前面 —— 静态库必须在目标文件之后
- ✅ 遇到循环依赖，先怀疑架构，再上 `--start-group`

## 关联项目

无

## 来源

GNU `ld` 手册「Archive members as needed」

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "错误码和异常，SDK 接口该怎么选？",
        "diff": 2,
        "body": """## 题目

**场景**：你在设计一个新 SDK，团队里有人主张全用异常（代码干净），
有人主张全用错误码（客户好接）。

**问**：你怎么定？

## 口述答案

**要点**

- **跨 ABI 边界 → 错误码**。异常跨编译器/跨版本不保证兼容，这是硬约束。
- **库内部 → 可以全用异常**，在边界处统一翻译成错误码。
- 如果 SDK 只在同一套工具链内部用（比如公司内部服务），全用异常也可以，但要在文档里写死这个前提。

## 讲深一层

两种风格的取舍：

| 维度 | 错误码 | 异常 |
|---|---|---|
| 跨语言/跨编译器 | ✅ 天然安全 | ❌ 不保证 |
| 调用方是否可能忽略错误 | 可能（忘检查） | 不可能（不捕获就传播） |
| 性能 | 无异常开销 | 抛出时开销大，正常路径几乎零成本 |
| 代码整洁度 | 每层都要检查 | 集中处理 |
| 析构安全 | 手动清理 | RAII 自动 |

实践中的混合模式：

```cpp
// 内部抛异常
void Process() { if (bad) throw Error("..."); }

// 边界转错误码，并保留详情
MYLIB_API int ProcessSafe(char* err, size_t cap) noexcept {
    try { Process(); return 0; }
    catch (const Error& e) { snprintf(err, cap, "%s", e.what()); return 1; }
    catch (...) { return -1; }
}
```

## 高频追问

1. **错误码怎么设计才不用背？** —— 分层：0 成功，负数是库级错误，正数是业务错误；或者用 `enum class` + `to_string()`。
2. **异常在析构函数里抛会怎样？** —— 若栈正在展开，会直接 `std::terminate`。析构函数默认 `noexcept`，要么别抛，要么内部 catch。
3. **`std::error_code` 和 `std::expected` 怎么选？** —— `error_code` 适合与系统错误对接；`expected<T, E>`（C++23）适合返回值 + 错误的现代写法，但要注意 ABI。

## 易错点

- ❌ 混用但没约定边界 —— 客户端不知道该 catch 还是查返回值
- ❌ 错误码只给数字不给文档 —— 客户只能靠猜
- ✅ 定了就用到底，别一个接口一个风格

## 关联项目

无

## 来源

C++ 核心指南 E.2/E.3；Win32 / POSIX 错误码惯例

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "前置声明什么时候不能替代 include？",
        "diff": 2,
        "body": """## 题目

**场景**：为了减少编译依赖，你把头文件里的 `#include <vector>` 换成了
`class Widget;` 的前置声明。结果编译报错说「incomplete type」。

**问**：什么时候前置声明够用，什么时候必须 include？

## 口述答案

**要点**

- 前置声明只能用于**指针、引用、返回值声明**（不需要知道大小和布局的场景）。
- 只要编译器需要知道**大小、成员、继承关系、或按值传递**，就必须有完整定义。
- 记忆：**"用不用到 sizeof 或成员访问"** —— 用得到就必须 include。

## 讲深一层

必须 include 的场景：

| 场景 | 需要完整类型？ |
|---|---|
| `Widget* p;` 指针 | ❌ 前置声明够 |
| `Widget& r;` 引用 | ❌ 够 |
| `Widget f();` 函数声明返回 | ❌ 够（定义时才需要） |
| `Widget w;` 成员变量 | ✅ 必须完整 |
| `std::vector<Widget> v;` | ✅ C++17 前必须（`sizeof` 需要） |
| `class Derived : public Widget` | ✅ 必须完整 |
| `sizeof(Widget)` | ✅ 必须完整 |
| `p->method()` | ✅ 必须完整（要知道成员） |
| 模板参数 `std::unique_ptr<Widget>` | ⚠️ 声明可以，析构时必须完整 |

最后一条是 pimpl 的经典陷阱：`unique_ptr<Impl>` 的析构需要 `Impl` 完整，所以析构函数必须在 `.cpp` 里定义。

## 高频追问

1. **为什么 `vector<Widget>` 不能只前置声明？** —— C++17 前 `vector` 的析构需要 `Widget` 完整（要调它的析构），标准库实现会实例化。C++17 起对不完整类型的支持有改善，但仍不通用。
2. **前置声明标准库类型可以吗？** —— 不行。标准库类型在哪个头、有哪些默认模板参数都是实现细节，前置声明是未定义行为。
3. **怎么系统性地减少 include？** —— 用 `include-what-you-use`（IWYU）工具分析，它会告诉你哪些 include 是多余的。

## 易错点

- ❌ 给 `std::string` 写前置声明 —— 未定义行为
- ❌ 前置声明了但成员函数在头文件里内联调用了成员 —— 编译失败
- ✅ 头文件里能前置声明就前置声明，`.cpp` 里再 include 全的

## 关联项目

无

## 来源

C++ 标准不完整类型规则；`unique_ptr` 析构要求

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
    {
        "title": "怎么给一个 C++ 库做单元测试？依赖外部硬件怎么办？",
        "diff": 2,
        "body": """## 题目

**场景**：你的 SDK 依赖摄像头和推理引擎，跑在目标板上。想在 CI 里跑单元测试，
但 CI 机器没有摄像头也没有 NPU。

**问**：怎么设计才能测？测哪些？

## 口述答案

**要点**

- **把硬件和算法解耦**：定义一个采集接口 `class IFrameSource { virtual bool Grab(Frame&) = 0; }`，
  真实实现读摄像头，测试实现读图片文件或生成合成数据。
- 同理把推理引擎包成接口，测试用「假引擎」返回固定结果。
- 这样 90% 的逻辑（数据流、后处理、状态机、边界处理）可以在 CI 里跑，只有极少数端到端用例留给真机。

## 讲深一层

分层测试策略：

| 层 | 测什么 | 跑在哪 | 依赖 |
|---|---|---|---|
| 单元 | 后处理、坐标变换、状态机 | CI | 无 |
| 集成 | 采集→推理→输出链路 | CI（用假实现） | 无 |
| 端到端 | 真实延迟、精度 | 目标板 | 硬件 |

关键是**接口边界画在哪**。如果算法函数直接 `#include` 了摄像头 SDK，就没法测——这些依赖必须在编译期可替换。

## 高频追问

1. **假实现会不会掩盖真实问题？** —— 会，所以要保留少量端到端用例，且假实现的行为要尽量贴近真实（延迟、错误率）。
2. **怎么测时间相关的逻辑？** —— 把时钟也抽象成接口，测试里注入可控时钟，不要直接调 `std::chrono::steady_clock::now()`。
3. **C++ 用什么测试框架？** —— GoogleTest 最通用；轻量场景 Catch2 也行；追求零依赖可以用 doctest。

## 易错点

- ❌ 为了可测性到处加虚函数 —— 热路径会有开销，接口要开在合理粒度
- ❌ 只测正常路径 —— 边界（空帧、超时、模型加载失败）才是 bug 高发区
- ✅ 先问「这段逻辑的输入是什么」，能注入的就能测

## 关联项目

YOLO 部署（推理链路的分层测试）

## 来源

依赖注入与测试替身；GoogleTest 文档

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
""",
    },
]

FM = """---
id: {qid}
title: {title}
module: 02_cpp
sub: {sub}
priority: P0
difficulty: {diff}
roles: [SDK开发, 系统工程]
companies: []
qtype: principle
status: draft
source_type: inferred
source_ref: 按 SDK / 基础软件岗位能力项整理
verified_at: 2026-11-09
tags: [SDK, 动态库, ABI, 接口设计, 工程化]
auto: true
sdk_seed: true
---

{body}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    removed = 0
    for f in CONTENT.glob("Q-*.md"):
        if re.search(r"^sdk_seed: true", f.read_text(encoding="utf-8"), re.M):
            f.unlink()
            removed += 1
    if removed:
        print(f"清理旧 SDK 题卡 {removed} 张")

    nums = [int(m.group(1)) for f in CONTENT.glob("Q-*.md")
            if (m := re.match(r"Q-(\d+)", f.name))]
    nxt = max(nums + [ID_BASE]) + 1
    start = nxt

    for it in ITEMS:
        if nxt >= ID_BASE + SPAN:
            print(f"⚠ 号段用尽，停在 {nxt}")
            return 1
        qid = f"Q-{nxt:04d}"
        if not args.dry:
            (CONTENT / f"{qid}-sdk.md").write_text(
                FM.format(qid=qid, title=it["title"], sub=SUB,
                          diff=it["diff"], body=it["body"]), encoding="utf-8")
        nxt += 1

    print(f"{'预览' if args.dry else '生成'} {len(ITEMS)} 道 → Q-{start:04d} ~ Q-{nxt-1:04d}  sub={SUB}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
