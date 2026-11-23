#from .maze_generator import Cell, MazeGenerator
from mlx import Mlx


CELL_SIZE: int = 50


COLOR: dict[str, int] = {
    "red" : 0xFFFF0000,
    "green" : 0xFF00FF00,
    "blue" : 0xFF0000FF,
    "white" : 0xFFFFFFFF,
    "black" : 0xFF000000
}

class Display:
    def __init__(self) -> None:
        self.mlx = Mlx()
        self.width = 800
        self.height = 600
        self.mlx_ptr = self.mlx.mlx_init()

        self.window = self.mlx.mlx_new_window(
            self.mlx_ptr,
            self.width,
            self.height,
            "My first MLX window"
        )

        # Register callbacks
        self.mlx.mlx_key_hook(
            self.window,
            self.on_key,
            None
        )

        self.mlx.mlx_hook(
            self.window,
            33,
            0,
            self.on_close,
            None
        )

        self.image = self.mlx.mlx_new_image(
        self.mlx_ptr,
        self.width,
        self.height
    )

        if self.image is None:
            raise RuntimeError("Could not create MLX image")

        (
            self.pixels,
            self.bits_per_pixel,
            self.size_line,
            self.image_format
        ) = self.mlx.mlx_get_data_addr(self.image)

        print("Bits per pixel:", self.bits_per_pixel)
        print("Bytes per pixel:", self.bits_per_pixel // 8)
        print("Bytes per row:", self.size_line)
        print("Image format:", self.image_format)
        print("Buffer length:", len(self.pixels))

    def on_key(self, key: int, _param) -> None:
        if key == 65307:  # Escape
            self.mlx.mlx_loop_exit(self.mlx_ptr)

    def on_close(self, _param) -> None:
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def draw_pixel(self, x: int, y: int, color: int) -> None:
        self.mlx.mlx_pixel_put(self.mlx_ptr, self.window, x, y, color)

    def draw_h_line(self, x: int, y: int, size: int, color: int) -> None:
        for i in range(size):
            if x + i >= self.width:
                break
            self.draw_pixel(x + i, y, color)

    def draw_v_line(self, x: int, y: int, size: int, color: int) -> None:
        for i in range(size):
            if y + i >= self.height:
                break
            self.draw_pixel(x, y + i, color)

    def draw_rectangle(self, x: int, y: int, width: int, height: int, color: int) -> None:
        self.draw_h_line(x, y, width, color)
        self.draw_v_line(x, y, height, color)
        self.draw_h_line(x, y + height - 1, width, color)
        self.draw_v_line(x + width - 1, y, height, color)

    def draw_fill_rectangle(self, x: int, y: int, width: int, height: int, color: int) -> None:
        self.draw_h_line(x, y, width, color)
        self.draw_v_line(x, y, height, color)
        self.draw_h_line(x, y + height - 1, width, color)
        self.draw_v_line(x + width - 1, y, height, color)
        for i in range(width):
            if i == 0 or i == width - 1:
                continue
            self.draw_v_line(x + i, y + 1, height - 2, COLOR["white"])


    def run(self) -> None:

        #self.draw_rectangle(100, 100, 300, 200, COLOR["red"])
        self.draw_fill_rectangle(100, 100, CELL_SIZE, CELL_SIZE, COLOR["white"])
        self.mlx.mlx_string_put(self.mlx_ptr, self.window, 100, 100, COLOR["white"], "ifjeworuv")
        self.mlx.mlx_loop(self.mlx_ptr)

        # Cleanup after the event loop exits
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.window)
        self.mlx.mlx_release(self.mlx_ptr)

        print("MLX closed successfully.")


def main() -> None:
    display = Display()
    display.run()



if __name__ == "__main__":
    main()
