import csv
from collections import defaultdict
from datetime import datetime as dt
from pathlib import Path

from pep_parse.constants import RESULTS_DIR_NAME

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    def open_spider(self, spider):
        self.statuses_count = defaultdict(int)
        self.total = 0

    def process_item(self, item, spider):
        self.statuses_count[item['status']] += 1
        self.total += 1
        return item

    def close_spider(self, spider):
        time_now = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'status_summary_{time_now}.csv'
        results_dir = BASE_DIR / RESULTS_DIR_NAME
        results_dir.mkdir(exist_ok=True)
        path = results_dir / filename

        with open(path, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f, lineterminator='\n')
            data = [('Статус', 'Количество')]
            data.extend((status, count) for status, count in self.statuses_count.items())
            data.append(('Total', self.total))
            writer.writerows(data)
