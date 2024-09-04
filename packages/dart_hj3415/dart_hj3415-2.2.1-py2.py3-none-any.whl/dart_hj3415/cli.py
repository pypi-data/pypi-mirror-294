import argparse
from dart_hj3415 import opendart
from db_hj3415 import mymongo, myredis
import pprint
from utils_hj3415 import noti


def save_today_darts(data_from_file=False) -> int:
    """
    오늘 공시 데이터를 수집해서 후처리후 몽고디비에 저장한다.
    :param data_from_file: 파일로 저장된 데이터를 사용한다.(디버깅용)
    :return: 저장된 총 공시개수 반환
    """
    if data_from_file:
        print(f"공시 데이터를 {opendart.OverView.SAVEFILENAME} 파일에서 가져옵니다.")
        import json
        # JSON 파일에서 리스트 불러오기
        with open(opendart.OverView.SAVEFILENAME, 'r') as file:
            overviews = json.load(file)
    else:
        overviews = opendart.OverView().get(save_to_file=True)
    print(f"총 {len(overviews)}의 데이터가 수집 되었습니다.")
    data = opendart.PostProcess.all_in_one(overviews)
    print("원본 데이터에서 후처리를 시행합니다...")

    # redis에 오늘 수집한 전체를 캐시로 저장
    myredis.DartToday().save(data)
    print(f"총 {len(data)}개의 공시를 redis에 저장했습니다.")

    # mongodb에 각 종목별로 나눠서 저장
    for item in data:
        mymongo.Dart.save(item['stock_code'], item)
    pprint.pprint(data)
    print(f"총 {len(data)}개의 공시를 각 종목별로 mongodb에 저장했습니다.")
    return len(data)


def dart():
    commands = {
        'save': save_today_darts,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('command', help=f"Commands - {commands.keys()}")
    parser.add_argument('--noti', action='store_true', help='작업완료후 메시지 전송여부')

    args = parser.parse_args()

    if args.command in commands.keys():
        if args.command == 'save':
            num_items = commands['save']()
            if args.noti:
                noti.telegram_to('manager', f"오늘 현재까지 {num_items}개의 공시를 저장했습니다.")
    else:
        print(f"The command should be in {list(commands.keys())}")
