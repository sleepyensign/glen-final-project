import pygame

def plrColStatic(plrRect, static, oldPos):
    overlap_left = plrRect.right - static.left
    overlap_right = static.right - plrRect.left
    overlap_top = plrRect.bottom - static.top
    overlap_bottom = static.bottom - plrRect.top

    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

    if min_overlap == overlap_left:
        plrRect.right = static.left
    elif min_overlap == overlap_right:
        plrRect.left = static.right
    elif min_overlap == overlap_top:
        plrRect.bottom = static.top
    else:
        plrRect.top = static.bottom