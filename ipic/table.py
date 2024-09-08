#*~------------------------~( Credit to stackoverflow, edited )~-----------------------------~*#
def table(rows):
  # find the max length of each column
  max_col_lens = list(map(max, zip(*[(len(str(cell)) for cell in row) for row in rows])))

  row_fstring = '   '.join("{: <%s}" % n for n in max_col_lens)
  
  retval = []
  for i, row in enumerate(rows):
    retval.append(row_fstring.format(*map(str, row)))
  return "\n".join(retval)
def htable(head, rows):
  # find the max length of each column
  max_col_lens = list(map(max, zip(*[(len(str(cell)) for cell in row) for row in rows])))

  row_fstring = '   '.join("{: <%s}" % n for n in max_col_lens)
  head_fstring = '___'.join("{:_<%s}" % n for n in max_col_lens)
  
  retval = []
  retval.append(head_fstring.format(*map(str, head)))
  for i, row in enumerate(rows):
    retval.append(row_fstring.format(*map(str, row)))
  return "\n".join(retval)
#*~--------------------------------~( End of credit )~---------------------------------------~*#