def progress(block_count, block_size, total_size):
  ratio = block_count * block_size / total_size
  if ratio > 1.0:
    percentage = 1.0
  max_bar = 50
  bar_num = int(ratio*max_bar)
  progress_element = '▮' * bar_num
  bar_fill = ' '
  bar = progress_element.ljust(max_bar, bar_fill)
  total_size_mb = total_size / 1024 /1024
  print(f'[{bar}] {ratio*100:.2f}% ( {total_size_mb:.0f}MB )\r',end='')
