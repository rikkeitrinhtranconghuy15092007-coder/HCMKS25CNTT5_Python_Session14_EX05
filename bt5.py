# =====================================================
# HỆ THỐNG NGÂN HÀNG ĐIỂM SỐ RIKKEI ACADEMY
# =====================================================
# Phân tích & Thiết kế Giải pháp (Tích hợp trực tiếp)

"""
(1) PHÂN TÍCH INPUT/OUTPUT & THIẾT KẾ GIẢI PHÁP

=== Input/Output Tổng quát ===
- Input chính: student_records (list of dict) - được truyền bằng reference → các hàm có thể sửa trực tiếp dữ liệu.
- Output: In thông báo giao diện console + cập nhật dữ liệu trong records.

=== Modular Design - Hàm phụ trợ ===
- find_student(records, student_id): Trả về index hoặc -1
  → Lợi ích:
    1. Tránh lặp lại logic tìm kiếm ở 4 chức năng (DRY principle)
    2. Chuẩn hóa mã học viên (upper case) ở một nơi
    3. Dễ bảo trì, dễ test, dễ mở rộng sau này

=== Thiết kế Thuật toán (Pseudocode) ===

Chức năng 2 - Đổi điểm (redeem_rewards):
    BEGIN
        student_id = input()
        idx = find_student(student_id)
        IF idx == -1:
            print("Không tìm thấy hồ sơ!")
            RETURN
        points = int(input())
        IF points <= 0 OR points > current_points:
            print lỗi tương ứng
        ELSE:
            current_points -= points
            spent_points += points
            print giao dịch thành công
    END

Chức năng 5 - Chấm bài (grade_assignment):
    BEGIN
        student_id = input()
        idx = find_student(student_id)
        IF idx == -1: print lỗi; RETURN
        base_points = int(input())
        IF base_points <= 0: print lỗi
        ELSE:
            real_points = base_points * multiplier
            current_points += real_points
            print thông tin hệ số + điểm thực nhận
    END
"""

def find_student(records, student_id):
    """Hàm phụ trợ: Tìm học viên theo mã (chuẩn hóa upper case)"""
    student_id = student_id.strip().upper()
    for idx, student in enumerate(records):
        if student["student_id"] == student_id:
            return idx
    return -1


def display_statements(records):
    """Chức năng 1: Hiển thị sao kê điểm số"""
    print("\n--- SAO KÊ ĐIỂM SỐ ---")
    for i, student in enumerate(records, 1):
        points = student["current_points"]
        if points < 500:
            status = "Cần tích lũy thêm"
        elif points <= 1500:
            status = "Thành viên tiềm năng"
        else:
            status = "Thành viên ưu tú"
        
        print(f"{i}. Mã: {student['student_id']} | "
              f"Tên: {student['name']:20} | "
              f"Hiện có: {student['current_points']:4} | "
              f"Đã tiêu: {student['spent_points']:4} | "
              f"Hoàn trả: {student['refunded_points']:3} | "
              f"Hệ số: x{student['multiplier']:.1f} | "
              f"Trạng thái: {status}")
    print("----------------------")


def redeem_rewards(records):
    """Chức năng 2: Đổi điểm lấy phần thưởng"""
    student_id = input("Nhập mã học viên đổi quà: ").strip()
    idx = find_student(records, student_id)
    if idx == -1:
        print("Không tìm thấy hồ sơ học viên!")
        return
    
    student = records[idx]
    try:
        points_to_spend = int(input("Nhập số điểm cần tiêu: ").strip())
        if points_to_spend <= 0:
            print("Vui lòng nhập số nguyên dương!")
            return
        if points_to_spend > student["current_points"]:
            print("Số dư điểm không đủ để thực hiện giao dịch!")
            return
        
        student["current_points"] -= points_to_spend
        student["spent_points"] += points_to_spend
        print(f">> Giao dịch thành công! '{student['name']}' đã tiêu {points_to_spend} điểm. "
              f"Số dư còn lại: {student['current_points']} điểm.")
    except ValueError:
        print("Vui lòng nhập số nguyên hợp lệ!")


def appeal_score(records):
    """Chức năng 3: Phúc khảo bài thi (Hoàn điểm)"""
    student_id = input("Nhập mã học viên cần phúc khảo: ").strip()
    idx = find_student(records, student_id)
    if idx == -1:
        print("Không tìm thấy hồ sơ học viên!")
        return
    
    student = records[idx]
    try:
        points_to_refund = int(input("Nhập số điểm hoàn lại: ").strip())
        if points_to_refund <= 0:
            print("Vui lòng nhập số nguyên dương!")
            return
        if points_to_refund > student["spent_points"]:
            print("Không thể hoàn số điểm lớn hơn tổng điểm đã tiêu!")
            return
        
        student["spent_points"] -= points_to_refund
        student["current_points"] += points_to_refund
        student["refunded_points"] += points_to_refund
        print(f">> Hoàn điểm thành công! '{student['name']}' được cộng lại {points_to_refund} điểm.")
    except ValueError:
        print("Vui lòng nhập số nguyên hợp lệ!")


def activate_multiplier(records):
    """Chức năng 4: Kích hoạt hệ số nhân điểm"""
    student_id = input("Nhập mã học viên nhận hệ số: ").strip()
    idx = find_student(records, student_id)
    if idx == -1:
        print("Không tìm thấy hồ sơ học viên!")
        return
    
    student = records[idx]
    try:
        new_multiplier = float(input("Nhập hệ số nhân mới (1.0 - 3.0): ").strip())
        if not (1.0 <= new_multiplier <= 3.0):
            print("Hệ số nhân không hợp lệ. Chỉ chấp nhận số từ 1.0 đến 3.0")
            return
        student["multiplier"] = new_multiplier
        print(f">> Đã kích hoạt hệ số x{new_multiplier:.1f} cho học viên '{student['name']}'.")
    except ValueError:
        print("Hệ số nhân không hợp lệ. Chỉ chấp nhận số từ 1.0 đến 3.0")


def grade_assignment(records):
    """Chức năng 5: Chấm bài (thêm điểm)"""
    student_id = input("Nhập mã học viên vừa nộp bài: ").strip()
    idx = find_student(records, student_id)
    if idx == -1:
        print("Không tìm thấy hồ sơ học viên!")
        return
    
    student = records[idx]
    try:
        base_points = int(input("Nhập số điểm gốc đạt được: ").strip())
        if base_points <= 0:
            print("Vui lòng nhập số nguyên dương!")
            return
        
        real_points = int(base_points * student["multiplier"])
        student["current_points"] += real_points
        print(f">> Hệ số hiện tại của '{student['name']}' là x{student['multiplier']:.1f}. "
              f"Điểm thực nhận: {real_points}.")
        print(f">> Đã cộng {real_points} điểm vào tài khoản!")
    except ValueError:
        print("Vui lòng nhập số nguyên hợp lệ!")


def main():
    """Hàm chính: Điều hướng menu"""
    student_records = [
        {"student_id": "RA01", "name": "Nguyễn Văn Code", "current_points": 1500,
         "spent_points": 500, "refunded_points": 0, "multiplier": 1.0},
        {"student_id": "RA02", "name": "Trần Thị Bug", "current_points": 800,
         "spent_points": 1200, "refunded_points": 100, "multiplier": 1.5},
        {"student_id": "RA03", "name": "Lê Văn Fix", "current_points": 300,
         "spent_points": 0, "refunded_points": 0, "multiplier": 2.0}
    ]
    
    while True:
        print("\n===== HỆ THỐNG NGÂN HÀNG ĐIỂM SỐ RIKKEI ACADEMY =====")
        print("1. Hiển thị sao kê điểm số")
        print("2. Đổi điểm lấy phần thưởng")
        print("3. Phúc khảo bài thi (Hoàn điểm)")
        print("4. Kích hoạt (Hệ số nhân điểm)")
        print("5. Chấm bài (thêm điểm)")
        print("6. Thoát chương trình")
        print("=====================================================")
        
        choice = input("Chọn chức năng (1-6): ").strip()
        
        if choice == "1":
            display_statements(student_records)
        elif choice == "2":
            redeem_rewards(student_records)
        elif choice == "3":
            appeal_score(student_records)
        elif choice == "4":
            activate_multiplier(student_records)
        elif choice == "5":
            grade_assignment(student_records)
        elif choice == "6":
            print("Cảm ơn bạn đã sử dụng hệ thống. Hẹn gặp lại!")
            break
        else:
            print("Lựa chọn không hợp lệ! Vui lòng chọn từ 1-6.")


if __name__ == "__main__":
    main()