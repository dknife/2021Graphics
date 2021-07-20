from PyQt5.QtWidgets import QApplication, QWidget

# 콘솔 명령으로 인자를 넘겨줄 때 필요 - 당분간 우리는 사용하지 않음
import sys

# 애플리케이션은 하나의 QApplication 인스턴스가 필요
# sys.argv에는 명령행에서 입력된 인자를 담고 있음 이를 QApplication 인자에 넘김
# 인자를 사용하지 않을 경우 sys.argv 대신 빈 리스트인 []를 넘길 수도 있음
# app = QApplication([])
app = QApplication(sys.argv)

# Qt 위젯을 생성 - 우리가 윈도우로 사용할 첫 위젯
window = QWidget()
window.show()  # 기본적으로 화면에 나타나지 않게 설정되어 있어 보이게 변경

# 애플리케이션이 이벤트 루프에 들어가게 만든다.
app.exec()

