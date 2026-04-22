import unittest
from math import sqrt, isclose
from common.r3 import R3
from modification.polyedr import Facet
from tests.matchers import R3ApproxMatcher, R3CollinearMatcher


class TestVoid(unittest.TestCase):

    # Эта грань не является вертикальной
    def test_vertical01(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(3.0, 0.0, 0.0), R3(0.0, 3.0, 0.0)])
        self.assertFalse(f.is_vertical())

    # Эта грань вертикальна
    def test_vertical02(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(0.0, 0.0, 1.0), R3(1.0, 0.0, 0.0)])
        self.assertTrue(f.is_vertical())

    # Нормаль к этой грани направлена вертикально вверх
    def test_h_normal01(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(3.0, 0.0, 0.0), R3(0.0, 3.0, 0.0)])
        self.assertEqual(R3CollinearMatcher(f.h_normal()), R3(0.0, 0.0, 1.0))

    # Нормаль к этой грани тоже направлена вертикально вверх
    def test_h_normal02(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(0.0, 3.0, 0.0), R3(3.0, 0.0, 0.0)])
        self.assertEqual(R3CollinearMatcher(f.h_normal()), R3(0.0, 0.0, 1.0))

    # Для нахождения нормали к этой грани рекомендуется нарисовать картинку
    def test_h_normal03(self):
        f = Facet([R3(1.0, 0.0, 0.0), R3(0.0, 1.0, 0.0), R3(0.0, 0.0, 1.0)])
        self.assertEqual(R3CollinearMatcher(f.h_normal()), R3(1.0, 1.0, 1.0))

    # Для каждой из следующих граней сначала «вручную» находятся
    # внешние нормали к вертикальным плоскостям, проходящим через
    # рёбра заданной грани, а затем проверяется, что эти нормали
    # имеют то же направление, что и вычисляемые методом v_normals

    # Нормали для треугольной грани
    def test_v_normal01(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(3.0, 0.0, 0.0), R3(0.0, 3.0, 0.0)])
        normals = [R3(-1.0, 0.0, 0.0), R3(0.0, -1.0, 0.0), R3(1.0, 1.0, 0.0)]
        for t in zip(f.v_normals(), normals):
            self.assertEqual(R3CollinearMatcher(t[0]), t[1])

    # Нормали для квадратной грани
    def test_v_normal02(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(2.0, 0.0, 0.0),
                   R3(2.0, 2.0, 0.0), R3(0.0, 2.0, 0.0)])
        normals = [R3(-1.0, 0.0, 0.0), R3(0.0, -1.0, 0.0),
                   R3(1.0, 0.0, 0.0), R3(0.0, 1.0, 0.0)]
        for t in zip(f.v_normals(), normals):
            self.assertEqual(R3CollinearMatcher(t[0]), t[1])

    # Нормали для ещё одной треугольной грани
    def test_v_normal03(self):
        f = Facet([R3(1.0, 0.0, 0.0), R3(0.0, 1.0, 0.0), R3(0.0, 0.0, 1.0)])
        normals = [R3(0.0, -1.0, 0.0), R3(1.0, 1.0, 0.0), R3(-1.0, 0.0, 0.0)]
        for t in zip(f.v_normals(), normals):
            self.assertEqual(R3CollinearMatcher(t[0]), t[1])

    # Центр квадрата
    def test_center01(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(2.0, 0.0, 0.0),
                   R3(2.0, 2.0, 0.0), R3(0.0, 2.0, 0.0)])
        self.assertEqual(R3ApproxMatcher(f.center()), (R3(1.0, 1.0, 0.0)))

    # Центр треугольника
    def test_center02(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(3.0, 0.0, 0.0), R3(0.0, 3.0, 0.0)])
        self.assertEqual(R3ApproxMatcher(f.center()), (R3(1.0, 1.0, 0.0)))

#   --- Новые тесты: ---
    # 1. Тесты метода condition()
    def test_condition_good(self):
        """Центр и хотя бы одна вершина строго вне x^2+y^2=1"""
        verts = [R3(2.0, 0.0, 0.0), R3(3.0, 0.0, 0.0), R3(2.5, 1.5, 0.0)]
        f = Facet(verts)
        self.assertTrue(f.condition())

    def test_condition_center_inside(self):
        """Центр внутри круга, условие должно быть False"""
        verts = [R3(0.1, 0.0, 0.0), R3(1.5, 0.0, 0.0), R3(0.0, 1.5, 0.0)]
        f = Facet(verts)
        self.assertFalse(f.condition())

    def test_condition_all_inside(self):
        """Все точки внутри круга"""
        verts = [R3(0.2, 0.0, 0.0), R3(0.3, 0.0, 0.0), R3(0.0, 0.4, 0.0)]
        f = Facet(verts)
        self.assertFalse(f.condition())

    def test_condition_boundary_point(self):
        """Вершина точно на окружности (x^2+y^2=1) -> не считается 'хорошей'"""
        verts = [R3(1.0, 0.0, 0.0), R3(0.0, 1.0, 0.0), R3(0.7, 0.7, 0.0)]
        f = Facet(verts)
        # Если все вершины <= 1, условие должно быть False
        self.assertFalse(f.condition())

    # 2. Тесты расчёта площади
    def test_facet_area_positive(self):
        """Площадь треугольника в проекции при порядке вершин против часовой стрелки"""
        # Грань далеко от начала координат, чтобы condition() == True
        verts = [R3(3.0, 0.0, 0.0), R3(5.0, 0.0, 0.0), R3(3.0, 2.0, 0.0)]
        f = Facet(verts)
        # Ожидаемая площадь: 0.5 * |2*2| = 2.0
        self.assertAlmostEqual(f.area, 2.0)

    def test_facet_area_zero_when_bad(self):
        """Если условие 'хорошести' не выполняется, area должна быть 0 (согласно текущей реализации)"""
        verts = [R3(0.1, 0.0, 0.0), R3(0.2, 0.0, 0.0), R3(0.0, 0.3, 0.0)]
        f = Facet(verts)
        self.assertAlmostEqual(f.area, 0.0)