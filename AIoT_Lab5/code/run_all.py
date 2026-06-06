import os

def run_script(script_name):
    print(f"\n{'='*50}\n[RUNNING] {script_name}\n{'='*50}")
    # Kiểm tra xem file có tồn tại không trước khi chạy
    if not os.path.exists(script_name):
        print(f"LỖI: Không tìm thấy file {script_name}!")
        return False
        
    # Chạy script và kiểm tra mã lỗi trả về
    exit_code = os.system(f"python {script_name}")
    if exit_code != 0:
        print(f"LỖI: Script {script_name} dừng đột ngột!")
        return False
    return True

if __name__ == "__main__":
    # Đã thêm data_utils.py vào đầu danh sách
    scripts = [
        "data_utils.py",
        "train_baseline_mobilenetv2.py",
        "quantize_ptq.py",
        "quantize_qat.py",
        "evaluate_models.py",
        "benchmark.py"
    ]
    
    print("BẮT ĐẦU CHẠY PIPELINE LAB 5...")
    for script in scripts:
        success = run_script(script)
        if not success:
            print("\nDừng toàn bộ quá trình do có lỗi xảy ra.")
            break
    else:
        print("\nTẤT CẢ CÁC BƯỚC ĐÃ HOÀN THÀNH THÀNH CÔNG!")