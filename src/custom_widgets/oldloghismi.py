for index, n in enumerate(reversed(self._log)):
    cell_width = n.x2 - n.x1
    cell_start = n.x1
    cell_end = n.x2

    mystery_width = cell_width - int((float(cell_width * n.preview_percent)))
    known_width = cell_width - mystery_width

    draw_mystery_area = False
    if draw_mystery_area:
        # Draw the area where we don't have any preview bytes loaded
        cr.set_source_rgb(0.2, 0.2, 0.2)
        cr.move_to(cell_start, 0)
        cr.line_to(cell_start, height)
        cr.line_to(cell_start + float(mystery_width), height)
        cr.line_to(cell_start + float(mystery_width), 0)
        cr.line_to(cell_start, 0)
        cr.fill()

    if index == self.mouse_in_cell:
        cr.set_source_rgb(0.3, 0.3, 0.3)
        cr.move_to(cell_start, 0)
        cr.line_to(cell_start, height)
        cr.line_to(cell_end, height)
        cr.line_to(cell_end, 0)
        cr.line_to(cell_start, 0)
        cr.fill()

    log_lines_per_pixel = float(len(n.message_line_lengths)) / float(known_width)
    if log_lines_per_pixel < 1:
        raise Exception("Not implemented")

    minimum_render_width = 4  # Although this does provide more of an aestheticlly pleasing visual, it may
    # overlook patterns in the text. It may be important to look for patterns while
    # generating the list



    if n.render_line_heights is None:
        log_lines = len(n.message_line_lengths)
        render_lines_height = []

        while log_lines > 0:
            lines_sample_index_start = int(log_lines - (log_lines_per_pixel * minimum_render_width))
            lines_sample_index_end = int(
                log_lines - (log_lines_per_pixel * minimum_render_width) + (log_lines_per_pixel * minimum_render_width))

            lines_sample = n.message_line_lengths[lines_sample_index_start:lines_sample_index_end]
            lines_average_length = sum(lines_sample) / (log_lines_per_pixel * minimum_render_width)

            render_lines_height.append(lines_average_length)
            log_lines = log_lines - (log_lines_per_pixel * minimum_render_width)

        n.render_line_heights = render_lines_height
    else:
        render_lines_height = n.render_line_heights

    # Now render the damn lines!
    for indexy, d in enumerate(render_lines_height):
        if d == 0:
            continue
        coyl = 0.6  # float(float(indexy) / float(len(render_lines_height)))
        cr.set_source_rgb(coyl, coyl, coyl)
        line_start = cell_start + cell_width - known_width + (indexy * minimum_render_width)
        cr.move_to(line_start, height)
        cr.line_to(line_start, d * height)
        cr.line_to(line_start + minimum_render_width, d * height)
        cr.line_to(line_start + minimum_render_width, height)
        cr.line_to(cell_start, height)
        cr.fill()
        cr.new_path()

if self.view_area_center != -1:
    # Draw the red line
    cr.set_source_rgba(0.7, 0, 0, 0.7)
    cr.set_line_width(3)
    cr.move_to(self.view_area_center, 0)
    cr.line_to(self.view_area_center, height)
    cr.stroke()
    cr.set_line_width(1)

    # Draw the view area
    half_view_width = float(self.view_area_width) / 2

    cr.set_source_rgba(0.8, 0.8, 0.8, 0.3)
    cr.move_to(self.view_area_center - half_view_width, 0)
    cr.line_to(self.view_area_center - half_view_width, height)
    cr.line_to(self.view_area_center + half_view_width, height)
    cr.line_to(self.view_area_center + half_view_width, 0)
    cr.line_to(self.view_area_center - half_view_width, 0)
    cr.fill()



    def get_total_log_size(self):
        return sum(log.log_size for log in self._log)

    def update_log_render_size(self, width, height):
        self._last_render_size_width = width
        self._last_render_size_height = height

        byte_to_pixel = float(width - len(self._log)) / float(self.get_total_log_size())

        last_x_position = float(0)
        for log in reversed(self._log):
            x1 = last_x_position
            x2 = last_x_position + log.log_size * byte_to_pixel

            log.x1 = int(x1)
            log.x2 = int(x2)
            last_x_position = x2 + 1



    def mouse_move(self, widget, event):
        # Find what cell the mouse is in
        # for index, n in enumerate(reversed(self._log)):
        #     cell_start = n.x1
        #     cell_end = n.x2
        #     if event.x >= cell_start and event.x < cell_end:
        #         self.mouse_in_cell = index
        #         self.queue_draw()
        # if self.button1_down == True and self.view_area_center != event.x:
        #     self.view_area_center = event.x
        #     self.queue_draw()


class LogRegion:
    preview_percent = property((lambda self: float(self.preview_bytes) / float(self.log_size)),
                               None,
                               None,
                               None)
    log_size = int

    def __init__(self, log_bytes):
        self.log_size = log_bytes
        self.message_line_lengths = []
        self.preview_bytes = 0
        self.render_line_heights = None

        # float(log_bytes * 0.5), [random.randrange(1, 101, 1) for _ in range(100)]
        noisy_preview = []
        remaining = log_bytes

        while (remaining > 0):
            noise = random.randrange(0, 200)
            if noise > remaining:
                noise = remaining

            noisy_preview.append(noise)
            remaining = remaining - noise

        self.append_preview(noisy_preview)

    def append_preview(self, preview_list):
        # preview_list is an array of [len(message)]
        max_in_list = max(preview_list)
        preview_bytes = sum(preview_list)

        for n in preview_list:
            preview_percent = n / max_in_list
            self.message_line_lengths.append(preview_percent)
        self.preview_bytes = self.preview_bytes + preview_bytes
