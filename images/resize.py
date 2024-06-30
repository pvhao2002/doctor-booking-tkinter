import cv2

img = cv2.imread('login_btn.jpg')

# crop top and bottom
left = img.shape[1] // 2
upper = 125
right = img.shape[1]
lower = 220
img = img[upper:lower, 0:right]

# resize 125x41
img = cv2.resize(img, (125, 21))

# save image
cv2.imwrite('login.png', img)
