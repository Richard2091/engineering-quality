#!/usr/bin/env python3
"""校验工程化质量 Skill 的结构、编码、引用、模板和规模约束。"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/baseline/universal.md",
    "references/workflows/implementation.md",
    "references/workflows/review.md",
    "references/workflows/remediation.md",
    "references/skill-maintenance.md",
    "references/roadmap.md",
    "references/templates/project-profile-template.md",
    "references/templates/implementation-plan-template.md",
    "references/templates/review-report-template.md",
    "references/templates/remediation-plan-template.md",
    "references/templates/release-gate-template.md",
    "references/templates/change-summary-template.md",
}

TEMPLATE_MARKERS = {
    "project-profile-template.md": ("项目类型", "风险等级", "待确认事项"),
    "implementation-plan-template.md": ("影响模块", "变更计划", "回滚"),
    "review-report-template.md": ("总体结论", "问题清单", "整改计划"),
    "remediation-plan-template.md": ("问题编号", "验证命令", "复审结论"),
    "release-gate-template.md": ("发布门禁", "发布结论", "回滚"),
    "change-summary-template.md": ("变更目的", "验证与交付", "剩余风险"),
}


class 结构校验器:
    """执行 Skill 的确定性结构校验，并汇总错误与警告。"""

    def __init__(self, 根目录: Path) -> None:
        self.根目录 = 根目录
        self.错误: list[str] = []
        self.警告: list[str] = []

    def 记录错误(self, 消息: str) -> None:
        """记录会导致校验失败的问题。"""
        self.错误.append(消息)

    def 记录警告(self, 消息: str) -> None:
        """记录不一定阻断校验的维护提示。"""
        self.警告.append(消息)

    def 校验必需文件(self) -> None:
        """检查索引和流程依赖的文件是否存在。"""
        for 相对路径 in sorted(REQUIRED_FILES):
            if not (self.根目录 / 相对路径).is_file():
                self.记录错误(f"缺少必需文件：{相对路径}")

    def 校验编码(self) -> None:
        """检查文本文件能否严格按 UTF-8 解码。"""
        for 文件 in self.根目录.rglob("*"):
            if ".git" in 文件.parts:
                continue
            if not 文件.is_file() or 文件.suffix.lower() not in {".md", ".yaml", ".yml", ".py"}:
                continue
            try:
                文件.read_bytes().decode("utf-8")
            except UnicodeDecodeError as 异常:
                self.记录错误(f"文件不是有效 UTF-8：{文件.relative_to(self.根目录)}，{异常}")

    def 校验引用(self) -> None:
        """解析 Markdown 相对链接并确认目标存在。"""
        链接模式 = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for 文件 in self.根目录.rglob("*.md"):
            if ".git" in 文件.parts:
                continue
            文本 = 文件.read_text(encoding="utf-8")
            for 目标 in 链接模式.findall(文本):
                if "://" in 目标 or 目标.startswith("#"):
                    continue
                目标路径 = 目标.split("#", 1)[0].strip()
                if not 目标路径:
                    continue
                解析路径 = (文件.parent / 目标路径).resolve()
                try:
                    解析路径.relative_to(self.根目录.resolve())
                except ValueError:
                    self.记录错误(f"引用越界：{文件.relative_to(self.根目录)} -> {目标}")
                    continue
                if not 解析路径.is_file():
                    self.记录错误(f"引用目标不存在：{文件.relative_to(self.根目录)} -> {目标}")

    def 校验规模(self) -> None:
        """检查入口、参考文件和目录是否出现明显失控。"""
        入口 = self.根目录 / "SKILL.md"
        if 入口.is_file() and len(入口.read_text(encoding="utf-8").splitlines()) > 350:
            self.记录错误("SKILL.md 超过 350 行，应把条件性规则移入 references。")
        for 文件 in self.根目录.rglob("*.md"):
            if ".git" in 文件.parts:
                continue
            if 文件.name == "SKILL.md":
                continue
            if len(文件.read_text(encoding="utf-8").splitlines()) > 400:
                self.记录警告(f"参考文件超过 400 行，请评估拆分：{文件.relative_to(self.根目录)}")
        for 目录 in [self.根目录, *[路径 for 路径 in self.根目录.rglob("*") if 路径.is_dir() and ".git" not in 路径.parts]]:
            直接文件数 = sum(1 for 子项 in 目录.iterdir() if 子项.is_file())
            if 直接文件数 > 12:
                self.记录警告(f"目录直接文件数为 {直接文件数}，请评估分组：{目录.relative_to(self.根目录)}")

    def 校验模板(self) -> None:
        """检查模板是否包含能够支撑闭环的实际字段。"""
        模板目录 = self.根目录 / "references/templates"
        for 文件名, 标记组 in TEMPLATE_MARKERS.items():
            文件 = 模板目录 / 文件名
            if not 文件.is_file():
                continue
            文本 = 文件.read_text(encoding="utf-8")
            for 标记 in 标记组:
                if 标记 not in 文本:
                    self.记录错误(f"模板缺少字段“{标记}”：{文件.relative_to(self.根目录)}")

    def 运行(self) -> int:
        """按固定顺序执行检查并返回命令退出码。"""
        # 依次检查文件、编码、引用、规模和模板，便于定位失败原因。
        self.校验必需文件()
        self.校验编码()
        self.校验引用()
        self.校验规模()
        self.校验模板()
        for 消息 in self.警告:
            print(f"警告：{消息}")
        for 消息 in self.错误:
            print(f"错误：{消息}")
        if self.错误:
            print(f"结构校验失败：{len(self.错误)} 个错误，{len(self.警告)} 个警告。")
            return 1
        print(f"结构校验通过：{len(self.警告)} 个警告。")
        return 0


def main(参数: list[str]) -> int:
    """解析命令行参数并启动结构校验。"""
    # 读取待校验的 Skill 路径并返回确定性退出码。
    根目录 = Path(参数[1] if len(参数) > 1 else Path(__file__).parents[1]).resolve()
    return 结构校验器(根目录).运行()


if __name__ == "__main__":
    sys.exit(main(sys.argv))