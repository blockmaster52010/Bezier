import pygame as pg
import numpy as np

class Bezier:
    DRAW_FILL = 1
    DRAW_LINE = 2

    def __init__(self, control_points, resolution, flags):
        self.control_points = np.array(control_points, dtype=float)
        self.resolution = resolution
        self.selected_point = None
        self.show_points = True
        self.point_size = 5
        self.line_thickness = 2
        self.point_color = (255, 0, 0)
        self.line_color = (255, 255, 255)
        self.fill_color = (255, 255, 255)
        self.draw_type = "line"
        
        # Extract the degree from the flags
        self.degree = len(control_points)-1

        if flags & Bezier.DRAW_FILL:
            self.draw_fill = True
        else:
            self.draw_fill = False

        if flags & Bezier.DRAW_LINE:
            self.draw_outline = True
        else:
            self.draw_outline = False

    def lerp(self, v1, v2, t):
        return np.add(np.multiply(v1, 1 - t), np.multiply(v2, t))

    def bezier(self, t, points):
        if len(points) == 1:
            return points[0]
        else:
            return self.lerp(self.bezier(t, points[:-1]), self.bezier(t, points[1:]), t)

    def draw(self, screen):
        if self.degree == 1:
            pg.draw.line(screen, self.line_color, self.control_points[0], self.control_points[1], self.line_thickness)
        else:
            for t in range(self.resolution + 1):
                
                point = self.bezier(t / self.resolution, self.control_points)
                    
                # Draw curve and fill if required
                if t != 0:
                    if self.draw_fill:
                        pg.draw.polygon(screen, self.fill_color, [cache, point, self.control_points[-1]])
                    if self.draw_outline:
                        pg.draw.line(screen, self.line_color, cache, point, self.line_thickness)
                cache = point

        # Draw the control points if show_points is True
        if self.show_points:
            for point in self.control_points:
                pg.draw.circle(screen, self.point_color, point.astype(int), self.point_size)

    def handle_event(self, event):
        if self.show_points:  # Only handle events if control points are visible
            if event.type == pg.MOUSEBUTTONDOWN:
                for i, point in enumerate(self.control_points):
                    if np.linalg.norm(point - event.pos) < 10:
                        self.selected_point = i
                        break
            elif event.type == pg.MOUSEBUTTONUP:
                self.selected_point = None
            elif event.type == pg.MOUSEMOTION and self.selected_point is not None:
                self.control_points[self.selected_point] = event.pos
            return
        self.selected_point = None


# Usage example:
pg.init()

width, height = 800, 600
screen = pg.display.set_mode((width, height), pg.DOUBLEBUF)

flags = Bezier.DRAW_LINE | Bezier.DRAW_FILL  # Use FILL and LINE flags for drawing both fill and outline
bezier = Bezier([(200, 300), (300, 100), (500, 100), (600, 300)], 100, flags)
bezier.point_color = (0, 255, 0)  # Change point color to green
bezier.point_size = 8  # Change point size to 8 pixels
bezier.line_color = (0,255,255)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            bezier.show_points = not bezier.show_points
        bezier.handle_event(event)

    screen.fill((0, 0, 0))
    bezier.draw(screen)

    pg.display.flip()

pg.quit()
