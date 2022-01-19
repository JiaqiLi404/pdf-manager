import cv2.cv2 as cv2
import numpy as np


def rgbfilter(img, s1, e1, s2, e2, s3, e3):
    if s1 > e1:
        s1, e1 = e1, s1
    if s2 > e2:
        s2, e2 = e2, s2
    if s3 > e3:
        s3, e3 = e3, s3
    if s1 == e1 == -1:
        s1 = 0
        e1 = 255
    if s2 == e2 == -1:
        s2 = 0
        e2 = 255
    if s3 == e3 == -1:
        s3 = 0
        e3 = 255
    lower = np.array([s3, s2, s1])
    upper = np.array([e3, e2, e1])
    mask = cv2.inRange(img, lower, upper)  # lower20===>0,upper200==>0，lower～upper==>255
    mask1 = cv2.bitwise_not(mask)
    img[:, :, 2] = cv2.bitwise_and(img[:, :, 2], img[:, :, 2], mask=mask1) + mask
    img[:, :, 1] = cv2.bitwise_and(img[:, :, 1], img[:, :, 1], mask=mask1) + mask
    img[:, :, 0] = cv2.bitwise_and(img[:, :, 0], img[:, :, 0], mask=mask1) + mask

    return img


def hsvfilter(img, s1, e1, s2, e2, s3, e3):
    if s1 > e1:
        s1, e1 = e1, s1
    if s2 > e2:
        s2, e2 = e2, s2
    if s3 > e3:
        s3, e3 = e3, s3
    if s1 == e1 == -1:
        s1 = 0
        e1 = 255
    if s2 == e2 == -1:
        s2 = 0
        e2 = 255
    if s3 == e3 == -1:
        s3 = 0
        e3 = 255
    lower = np.array([s1, s2, s3])
    upper = np.array([e1, e2, e3])
    mask = cv2.inRange(img, lower, upper)
    mask1 = cv2.bitwise_not(mask)
    img[:, :, 2] = cv2.bitwise_and(img[:, :, 2], img[:, :, 2], mask=mask1) + mask
    img[:, :, 1] = cv2.bitwise_and(img[:, :, 1], img[:, :, 1], mask=mask1)
    img[:, :, 0] = cv2.bitwise_and(img[:, :, 0], img[:, :, 0], mask=mask1)

    return img


def setwhite(img, x1, y1, x2, y2):
    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), -1)
    return img


def sharpenimg(img, alpha, belta):
    # cv2.imshow('img', img)
    blank = np.zeros(img.shape, img.dtype)
    # dst = alpha * img + (1-alpha) * blank + beta
    img = cv2.addWeighted(img, alpha, blank, 1 - alpha, belta)
    # cv2.imshow('img2', img)
    # cv2.waitKey(0)
    return img
