import random
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from tjw.core.shengfenzheng.sfz import CShengFenZheng
from tjw.core.db import log_operation, record_sfz_generation, record_sfz_verification, get_statistics, get_db

router = APIRouter()

# 初始化身份证工具（避免循环导入）
sfz_tool = CShengFenZheng()

# 响应模型
class SFZResponse(BaseModel):
    success: bool = Field(description="操作是否成功")
    message: str = Field(description="提示信息")
    data: Optional[dict] = Field(None, description="返回数据")

class SFZGenerateResponse(BaseModel):
    success: bool = True
    message: str = "生成成功"
    data: dict = Field(description="身份证信息")

class SFZVerifyResponse(BaseModel):
    success: bool = Field(description="验证是否通过")
    message: str = Field(description="验证结果信息")
    data: Optional[dict] = Field(None, description="身份证详细信息")

class SFZBatchResponse(BaseModel):
    success: bool = True
    message: str = "批量生成成功"
    data: List[dict] = Field(description="身份证列表")

# 生成单个身份证
@router.get("/generate", response_model=SFZGenerateResponse, summary="生成单个身份证")
async def generate_sfz(
    sex: Optional[str] = Query(None, description="性别: male/female/None(随机)"),
    region: Optional[str] = Query(None, description="地区编码(6位数字)，如110000表示北京"),
    birth_date: Optional[str] = Query(None, description="出生日期(YYYYMMDD格式)")
):
    """
    生成一个18位身份证号
    
    - **sex**: 可选参数，指定性别 male(男)/female(女)，不指定则随机
    - **region**: 可选参数，指定地区编码(6位数字)，如110000表示北京，不指定则随机
    - **birth_date**: 可选参数，指定出生日期(YYYYMMDD格式)，不指定则随机
    """
    new_id = sfz_tool.rnd_sfz18()
    
    # 如果指定地区，使用指定的地区编码
    if region and len(region) == 6 and region.isdigit():
        new_id = region + new_id[6:]
    
    # 如果指定出生日期，使用指定的出生日期
    if birth_date and len(birth_date) == 8 and birth_date.isdigit():
        new_id = new_id[:6] + birth_date + new_id[14:]
    
    # 如果指定性别，重新生成顺序码直到满足条件
    if sex:
        max_attempts = 100
        attempts = 0
        while attempts < max_attempts:
            gender_bit = int(new_id[16])
            is_male = gender_bit % 2 == 1
            
            if (sex == "male" and is_male) or (sex == "female" and not is_male):
                break
            
            # 只重新生成顺序码部分(14-16位)
            new_id = new_id[:14] + str(random.randint(100, 999)).zfill(3) + new_id[17:]
            attempts += 1
    
    # 重新计算校验码
    new_id = new_id[:17] + sfz_tool._get_yzm(new_id[:17])
    
    diqu = sfz_tool.get_diqu(new_id)
    verify_result = sfz_tool.sfz_yz(new_id)
    
    gender = "男" if int(new_id[16]) % 2 == 1 else "女"
    
    record_sfz_generation(
        id_number=new_id,
        region=diqu,
        birth_date=f"{new_id[6:10]}-{new_id[10:12]}-{new_id[12:14]}",
        gender=gender
    )
    log_operation('generate', 'sfz', f'生成身份证: {new_id[:6]}****{new_id[-4:]}')
    
    return {
        "success": True,
        "message": "生成成功",
        "data": {
            "id_number": new_id,
            "formatted": f"{new_id[:6]} {new_id[6:14]} {new_id[14:]}",
            "region": diqu,
            "birth_date": f"{new_id[6:10]}-{new_id[10:12]}-{new_id[12:14]}",
            "gender": gender,
            "verified": verify_result == ""
        }
    }

# 批量生成身份证
@router.get("/generate/batch", response_model=SFZBatchResponse, summary="批量生成身份证")
async def generate_sfz_batch(
    count: int = Query(10, description="生成数量(1-100)", ge=1, le=100)
):
    """
    批量生成多个身份证号
    
    - **count**: 生成数量，范围1-100，默认10
    """
    result = []
    
    for _ in range(count):
        new_id = sfz_tool.rnd_sfz18()
        diqu = sfz_tool.get_diqu(new_id)
        
        result.append({
            "id_number": new_id,
            "region": diqu,
            "birth_date": f"{new_id[6:10]}-{new_id[10:12]}-{new_id[12:14]}",
            "gender": "男" if int(new_id[16]) % 2 == 1 else "女"
        })
    
    return {
        "success": True,
        "message": f"成功生成{count}个身份证",
        "data": result
    }

# 验证身份证
@router.get("/verify", response_model=SFZVerifyResponse, summary="验证身份证")
async def verify_sfz(id_number: str = Query(..., description="18位身份证号")):
    """
    验证身份证号的有效性
    
    - **id_number**: 18位身份证号
    """
    id_number = id_number.replace(" ", "").upper()
    
    if len(id_number) != 18:
        return {
            "success": False,
            "message": "身份证号位数不正确",
            "data": None
        }
    
    errors = sfz_tool.sfz_yz(id_number)
    
    if errors:
        return {
            "success": False,
            "message": errors,
            "data": None
        }
    
    diqu = sfz_tool.get_diqu(id_number)
    gender = "男" if int(id_number[16]) % 2 == 1 else "女"
    
    record_sfz_verification(
        id_number=id_number,
        region=diqu,
        birth_date=f"{id_number[6:10]}-{id_number[10:12]}-{id_number[12:14]}",
        gender=gender
    )
    log_operation('verify', 'sfz', f'验证身份证: {id_number[:6]}****{id_number[-4:]}')
    
    return {
        "success": True,
        "message": "验证通过",
        "data": {
            "id_number": id_number,
            "region": diqu,
            "birth_date": f"{id_number[6:10]}年{id_number[10:12]}月{id_number[12:14]}日",
            "gender": gender
        }
    }

# 查询归属地
@router.get("/region", response_model=SFZResponse, summary="查询归属地")
async def get_region(id_number: str = Query(..., description="身份证号（至少前6位）")):
    """
    查询身份证号对应的归属地
    
    - **id_number**: 身份证号，至少需要前6位
    """
    id_number = id_number.replace(" ", "")
    
    if len(id_number) < 6:
        return {
            "success": False,
            "message": "至少需要输入6位",
            "data": None
        }
    
    diqu = sfz_tool.get_diqu(id_number)
    
    return {
        "success": True,
        "message": "查询成功",
        "data": {
            "id_prefix": id_number[:6],
            "region": diqu
        }
    }

# 获取所有地区列表
@router.get("/regions", response_model=SFZResponse, summary="获取所有地区列表")
async def get_all_regions():
    """
    获取系统支持的所有地区编码和名称
    """
    regions = []
    for code, name in sfz_tool.coll_diqu.items():
        regions.append({
            "code": code,
            "name": name
        })
    
    return {
        "success": True,
        "message": "获取成功",
        "data": {
            "count": len(regions),
            "regions": regions
        }
    }

# 获取统计信息
@router.get("/stats", response_model=SFZResponse, summary="获取统计信息")
async def get_sfz_stats():
    """
    获取身份证工具的统计信息
    """
    stats = get_statistics()
    
    return {
        "success": True,
        "message": "获取成功",
        "data": {
            "total_generated": stats.get('sfz_records', 0),
            "total_operations": stats.get('operation_logs', 0),
            "total_settings": stats.get('user_settings', 0)
        }
    }

# 获取历史记录
@router.get("/history", response_model=SFZResponse, summary="获取生成历史记录")
async def get_sfz_history(
    limit: int = Query(20, description="返回数量", ge=1, le=100),
    offset: int = Query(0, description="偏移量", ge=0)
):
    """
    获取身份证生成历史记录
    """
    db = get_db()
    records = db.get_sfz_records(limit=limit, offset=offset)
    
    return {
        "success": True,
        "message": "获取成功",
        "data": {
            "count": len(records),
            "total": db.get_sfz_record_count(),
            "records": [record.to_dict() for record in records]
        }
    }