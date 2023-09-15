from dataclasses import dataclass
import pygame

@dataclass
class ScreenData():
    scale: int
    screen: pygame.Surface 
    width: int
    height: int
    edge: tuple[float,float] 

