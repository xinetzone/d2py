"""任务型事务辅助函数"""
import asyncio

async def run_cmd(cmd: str, cwd: str=".", **kwds):
    """运行命令行执行任务

    Args:
        cmd: 命令行任务
        cwd: 当前工作目录
    """
    proc = await asyncio.create_subprocess_shell(
        cmd, 
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd, **kwds)
    stdout, stderr = await proc.communicate(input=None)
    std_data = f'[{cmd!r} 退出状态码 {proc.returncode}]\n'
    if stdout:
        std_data += f'[stdout]:\n{stdout}\n'
    if stderr:
        std_data += f'[stdinfo]:\n{stderr}\n'
    return std_data
