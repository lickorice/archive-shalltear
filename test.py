from data import linv

invManager = linv.LickInventory()

invManager.init()

invManager.rm_item("Carlos", ['one', 1, True])
print(invManager.get_items("Carlos"))