import csv
from PIL import Image, ImageDraw


class MarsMapVisualizer:
    def __init__(self, csv_path, cell_size=40):
        self.csv_path = csv_path
        self.grid = []
        self.cell_size = cell_size
        self.max_x = 0
        self.max_y = 0

    def load_data(self):
        """
        CSV 파일로부터 카테고리 데이터를 읽어 2차원 그리드 형태로 저장
        좌표는 (1,1)부터 시작한다고 가정
        """
        with open(self.csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            coords = []
            for row in reader:
                x = int(row['x'])
                y = int(row['y'])
                category = int(row['category'])
                coords.append((x, y, category))
                self.max_x = max(self.max_x, x)
                self.max_y = max(self.max_y, y)

            # 그리드 초기화
            self.grid = [[0 for _ in range(self.max_y)] for _ in range(self.max_x)]
            for x, y, category in coords:
                self.grid[x - 1][y - 1] = category  # 좌표 1부터 시작하므로 -1

    def draw_triangle(self, draw, cx, cy, size, fill_color):
        h = size * (3 ** 0.5) / 2
        triangle = [
            (cx, cy - 2 / 3 * h),
            (cx - size / 2, cy + h / 3),
            (cx + size / 2, cy + h / 3)
        ]
        draw.polygon(triangle, fill=fill_color)

    def draw_map(self, output_file='mars_map.png'):
        rows, cols = self.max_x, self.max_y
        width = cols * self.cell_size
        height = rows * self.cell_size

        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)

        for i in range(rows):
            for j in range(cols):
                category = self.grid[i][j]
                x = j * self.cell_size
                y = i * self.cell_size
                cx = x + self.cell_size // 2
                cy = y + self.cell_size // 2

                if category == 1:  # 암석: 갈색 원형
                    r = int(self.cell_size * 0.5)  # 살짝 겹치게 크게
                    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill='sienna')

                elif category == 2:  # 기타 구조물: 회색 사각형
                    margin = int(self.cell_size * 0.1)
                    draw.rectangle(
                        [x + margin, y + margin, x + self.cell_size - margin, y + self.cell_size - margin],
                        fill='gray'
                    )

                elif category == 3 or category == 4:  # 기지: 녹색 삼각형
                    size = self.cell_size * 0.8
                    self.draw_triangle(draw, cx, cy, size, fill_color='green')

                # 그리드 라인
                draw.rectangle([x, y, x + self.cell_size, y + self.cell_size], outline='black')

        img.save(output_file)
        print(f"✅ 지도가 저장되었습니다: {output_file}")


# ✅ 실행 예시
if __name__ == '__main__':
    csv_path = '/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_2/process_3/3-01/area_struct.csv'
    output_path = '/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_2/process_3/3-02/mars_map.png'

    visualizer = MarsMapVisualizer(csv_path)
    visualizer.load_data()
    visualizer.draw_map(output_path)
