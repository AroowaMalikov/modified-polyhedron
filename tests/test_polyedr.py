import unittest
from unittest.mock import patch, mock_open
import io
import sys

from modification.polyedr import Polyedr, Edge, Facet
from common.r3 import R3


class TestPolyedr(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        fake_file_content = """200.0	45.0	45.0	30.0
8	4	16
-0.5	-0.5	0.5
-0.5	0.5	0.5
0.5	0.5	0.5
0.5	-0.5	0.5
-0.5	-0.5	-0.5
-0.5	0.5	-0.5
0.5	0.5	-0.5
0.5	-0.5	-0.5
4	5    6    2    1
4	3    2    6    7
4	3    7    8    4
4	1    4    8    5"""
        fake_file_path = 'data/holey_box.geom'
        with patch('modification.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)

    def test_num_vertexes(self):
        self.assertEqual(len(self.polyedr.vertexes), 8)

    def test_num_facets(self):
        self.assertEqual(len(self.polyedr.facets), 4)

    def test_num_edges(self):
        self.assertEqual(len(self.polyedr.edges), 16)

# --- Новые тесты  

class MockTkDrawer:
    """Заглушка для TkDrawer, чтобы тесты не открывали графическое окно"""
    def clean(self): pass
    def draw_line(self, p1, p2): pass

class TestPolyedrAreaSum(unittest.TestCase):

    def test_draw_prints_correct_area(self):
        """Проверка, что draw() выводит сумму площадей 'хороших' граней"""
        # Создадим минимальный полиэдр вручную для контроля данных
        p = Polyedr.__new__(Polyedr)
        p.vertexes, p.edges, p.facets = [], [], []

        # Грань 1: "хорошая", площадь проекции = 2.0
        v1 = [R3(3.0, 0.0, 0.0), R3(5.0, 0.0, 0.0), R3(3.0, 2.0, 0.0)]
        p.facets.append(Facet(v1))
        # Грань 2: "плохая", площадь = 0 по логике condition()
        v2 = [R3(0.1, 0.0, 0.0), R3(0.2, 0.0, 0.0), R3(0.0, 0.3, 0.0)]
        p.facets.append(Facet(v2))
        # Рёбра не влияют на сумму площадей, но добавим для целостности
        p.edges = [Edge(v1[0], v1[1]), Edge(v1[1], v1[2]), Edge(v1[2], v1[0])]

        # Захватываем print()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        p.draw(MockTkDrawer())
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        
        self.assertAlmostEqual(float(output[26::]), 2.0)
