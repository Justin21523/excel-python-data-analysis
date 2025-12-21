#!/usr/bin/env python3
"""
Run All Capstone Projects
執行所有 Capstone 專案

Usage: python run_all.py [--sequential|--parallel] [--verbose]
"""

import sys
import os
import subprocess
import argparse
import logging
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CapstoneRunner:
    """Capstone 專案執行器"""

    def __init__(self, sequential=False, verbose=False):
        """
        初始化

        Args:
            sequential (bool): 是否順序執行
            verbose (bool): 是否詳細輸出
        """
        self.sequential = sequential
        self.verbose = verbose

        self.base_dir = Path(__file__).parent
        self.projects = [
            'project1_sales_intelligence',
            'project2_customer_insights',
            'project3_inventory_optimizer',
            'project4_operations_monitor',
            'project5_executive_dashboard'
        ]

        self.results = {}

    def run(self):
        """執行所有項目"""
        logger.info("=" * 60)
        logger.info("Week 15-20 Capstone Projects - 開始執行")
        logger.info("=" * 60)
        logger.info(f"執行模式: {'順序' if self.sequential else '並行'}")
        logger.info(f"項目數: {len(self.projects)}\n")

        start_time = datetime.now()

        try:
            if self.sequential:
                self._run_sequential()
            else:
                self._run_parallel()

            self._print_summary(start_time)
            return self._all_success()

        except Exception as e:
            logger.error(f"執行失敗: {e}", exc_info=self.verbose)
            return False

    def _run_sequential(self):
        """順序執行所有項目"""
        logger.info("順序執行項目...")

        for idx, project in enumerate(self.projects, 1):
            logger.info(f"\n[{idx}/{len(self.projects)}] 執行 {project}...")
            self._run_project(project)

    def _run_parallel(self):
        """並行執行所有項目"""
        logger.info("並行執行項目...")

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(self._run_project, project): project
                for project in self.projects
            }

            for future in as_completed(futures):
                project = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"{project} 執行失敗: {e}")

    def _run_project(self, project_name):
        """
        執行單個項目

        Args:
            project_name (str): 項目名稱
        """
        project_dir = self.base_dir / project_name
        main_file = project_dir / 'main.py'

        if not main_file.exists():
            logger.warning(f"{project_name} 的 main.py 不存在")
            self.results[project_name] = {
                'status': 'FAILED',
                'error': 'main.py 不存在'
            }
            return

        try:
            # 執行項目
            cmd = [sys.executable, str(main_file)]
            result = subprocess.run(
                cmd,
                cwd=str(project_dir),
                capture_output=not self.verbose,
                text=True,
                timeout=600  # 10 分鐘超時
            )

            if result.returncode == 0:
                logger.info(f"✓ {project_name} 執行成功")
                self.results[project_name] = {'status': 'SUCCESS'}
            else:
                logger.error(f"✗ {project_name} 執行失敗")
                if result.stderr:
                    logger.error(f"  錯誤: {result.stderr[:500]}")
                self.results[project_name] = {
                    'status': 'FAILED',
                    'error': result.stderr[:500]
                }

        except subprocess.TimeoutExpired:
            logger.error(f"✗ {project_name} 執行超時")
            self.results[project_name] = {
                'status': 'TIMEOUT',
                'error': '執行超過 10 分鐘'
            }

        except Exception as e:
            logger.error(f"✗ {project_name} 執行異常: {e}")
            self.results[project_name] = {
                'status': 'ERROR',
                'error': str(e)
            }

    def _print_summary(self, start_time):
        """打印摘要"""
        elapsed_time = datetime.now() - start_time

        logger.info("\n" + "=" * 60)
        logger.info("執行摘要")
        logger.info("=" * 60)

        success_count = sum(1 for r in self.results.values() if r['status'] == 'SUCCESS')
        failed_count = len(self.results) - success_count

        logger.info(f"成功: {success_count}/{len(self.results)}")
        logger.info(f"失敗: {failed_count}/{len(self.results)}")
        logger.info(f"用時: {elapsed_time.total_seconds():.2f} 秒")

        logger.info("\n詳細結果:")
        for project, result in self.results.items():
            status = result['status']
            symbol = "✓" if status == 'SUCCESS' else "✗"
            logger.info(f"  {symbol} {project}: {status}")

            if 'error' in result and result['error']:
                logger.info(f"    └─ {result['error'][:100]}")

    def _all_success(self):
        """檢查是否全部成功"""
        return all(r['status'] == 'SUCCESS' for r in self.results.values())


def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description='執行所有 Week 15-20 Capstone 專案'
    )

    parser.add_argument(
        '--sequential',
        action='store_true',
        default=False,
        help='順序執行（默認為並行）'
    )

    parser.add_argument(
        '--parallel',
        action='store_true',
        default=False,
        help='並行執行（默認）'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        default=False,
        help='詳細輸出'
    )

    parser.add_argument(
        '--project',
        type=str,
        help='執行指定項目'
    )

    args = parser.parse_args()

    # 決定執行模式
    sequential = args.sequential and not args.parallel

    # 創建執行器
    runner = CapstoneRunner(sequential=sequential, verbose=args.verbose)

    # 執行單個項目或全部
    if args.project:
        if args.project in runner.projects:
            runner._run_project(args.project)
            runner._print_summary(datetime.now())
            success = args.project in [k for k, v in runner.results.items() if v['status'] == 'SUCCESS']
        else:
            logger.error(f"未知的項目: {args.project}")
            logger.info(f"可用項目: {', '.join(runner.projects)}")
            success = False
    else:
        success = runner.run()

    # 返回退出碼
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
