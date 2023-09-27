import csv
from collections import defaultdict
from datetime import datetime as dt
from pathlib import Path


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
        path = BASE_DIR / 'results' / filename
        with open(path, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(('Статус', 'Количество'))
            for status, count in self.statuses_count.items():
                writer.writerow((status, count))
            writer.writerow(('Total', self.total))
