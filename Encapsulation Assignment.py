# 1. 캡슐화를 활용하는 클래스 생성
class BankAccount:
    def __init__(self, account_type, initial_balance):
        # 보호된(Protected) 속성: 싱글 언더스코어(_) 사용
        # 외부에서 접근할 수는 있지만, "건드리지 마시오"라는 암묵적인 경고를 의미합니다.
        self._account_type = account_type

        # 프라이빗(Private) 속성: 더블 언더스코어(__) 사용
        # 외부에서 직접 접근할 수 없도록 데이터를 안전하게 숨깁니다 (계좌 잔액 보호).
        self.__balance = initial_balance

    # 프라이빗 속성의 값을 안전하게 확인하기 위한 메서드
    def get_balance(self):
        print(f"현재 잔액은 ${self.__balance} 입니다.")

    # 프라이빗 속성의 값을 안전하게 변경하기 위한 메서드
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"{self._account_type} 계좌에 ${amount} 입금되었습니다.")


# 2. 객체 생성
my_account = BankAccount("Savings", 500)

# 3. 보호된(Protected) 속성 활용
# 파이썬에서는 접근 및 수정이 가능하지만, 규칙상 이렇게 직접 수정하는 것은 권장하지 않습니다.
print(f"보호된 속성 접근: {my_account._account_type}")
my_account._account_type = "Checking"  # 보호된 속성 변경
print(f"보호된 속성 변경 후: {my_account._account_type}")

print("-" * 30)

# 4. 프라이빗(Private) 속성 활용
# my_account.__balance를 직접 호출하면 에러가 발생하므로, 클래스 내부의 메서드를 사용해야 합니다.
my_account.get_balance()     # 프라이빗 속성 확인
my_account.deposit(150)      # 프라이빗 속성 변경 (입금)
my_account.get_balance()     # 변경된 프라이빗 속성 확인