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



