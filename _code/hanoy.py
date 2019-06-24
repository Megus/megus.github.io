def hanoy_recursive(disks, src, dst, hlp):
  if disks == 1:
    print(src, dst)
    return

  hanoy_recursive(disks - 1, src, hlp, dst)
  print(src, dst)
  hanoy_recursive(disks - 1, hlp, dst, src)

hanoy_recursive(6, 0, 2, 1)
