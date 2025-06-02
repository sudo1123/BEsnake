# -*- coding: UTF-8 -*-
# Copyright (c) 2025 QU QI
# MIT Licensed (https://opensource.org/licenses/MIT)
#导入引用
import turtle
import copy
import random
import json
import os
import keyboard
import time
#画面设置变量(由json文件加载)
Dot_Diameter=0#蛇&食物直径
Size=0#场地边长（需为直径整数倍且为偶数）
#配色方案
colors = {
    "game_background": "#0F172A",           # 深空蓝
    "scene_border": "#334155",              # 钢灰色
    "snake": "#00FFC6",                     # 赛博青
    "food": "#FFA726",                      # 琥珀橙
    "score": "#E4E7EB",                     # 月光白
    "GAME_OVER": "#F59E0B",                 # 落日金
    "end_screen_background": "#1E293B",     # 暗夜蓝
    "end_screen_score": "#38BDF8",          # 信号蓝
    "PRESS_ENTER_TO_RESTART": "#94A3B8",     # 月石灰
    "special_food":"red",
    "pause":"white"
}
#运行状态变量
initial_length=3#蛇的初始长度
Dot_Number=0#蛇长
food_exist=0#食物是否存在
special_food_exist=0#特殊食物是否存在
foodX_permanent=0#当前食物X坐标
foodY_permanent=0#当前食物Y坐标
Score=0#当前得分
Score_change=0#分数是否变化
elimination=0#是否淘汰
Restart=0#是否重来
special_foodX=0#特殊食物X坐标
special_foodY=0#特殊食物Y坐标
score_change_number=0#分数改变次数
special_food_start=0#特殊食物生成时间
direction_changed = False#方向是否改变(方向锁)
is_pause=0#是否暂停
timer_id =0#计时器ID
#初始化蛇长
Dot_Number=initial_length
def _main_ ():#全游戏主循环
    global Size,elimination,Score_change,Dot_Number,real_highest_score,Score,food_exist,frame_delay,Restart,foodX_permanent,foodY_permanent,initial_length,special_foodX,special_foodY,special_food_exist,special_food_start,is_pause,timer_id#全局申明
    turtle.clearscreen()
    turtle.bgcolor(colors["game_background"])#设置游戏背景颜色
    version="BEsnake-v1.8"#版本号兼标题
    screen = turtle.Screen()#创建窗口
    screen.title(version)#设置标题
    screen.listen()#启用键盘监听
    screen.tracer(0)  # 关闭自动刷新
    def init_files():#初始化文件函数
        # 初始化文件列表及默认值
        files = {
            "highest_score.json": 0,
            "frame_delay.json":0.2,
            "up_setting.json":"w",
            "down_setting.json":"s",
            "left_setting.json":"a",
            "right_setting.json":"d",
            "frame_size.json":450,
            "Dot_Diameter.json":10
        }   
        # 遍历创建文件
        for filename, default in files.items():
            if not os.path.exists(filename):
                with open(filename, "w", encoding="UTF-8") as f:
                    json.dump(default, f, ensure_ascii=False)
    init_files()#初始化创建文件
    #读取默认设置和最高分
    with open("highest_score.json","r") as HS:#读取历史最高分
        highest_score=json.load(HS)
    real_highest_score=highest_score
    with open("frame_size.json","r") as FZ:#读取边框边长设置
        Size=int(json.load(FZ))
    with open("Dot_Diameter.json","r") as DD:#读取蛇与食物直径设置
        Dot_Diameter=int(json.load(DD))
    with open("frame_delay.json","r") as FD:#读取帧间隔设置（秒）**本变量同样决定蛇的移动速度，不宜设得过小**
        frame_delay=json.load(FD)
    with open("up_setting.json","r") as US:#读取上键键位设置
        up_setting=json.load(US)
    with open("down_setting.json","r") as DS:#读取下键键位设置
        down_setting=json.load(DS)
    with open("left_setting.json","r") as LS:#读取左键键位设置
        left_setting=json.load(LS)
    with open("right_setting.json","r") as RS:#读取右键键位设置
        right_setting=json.load(RS)
    #特殊画笔（这个画笔没有任何实际作用，它唯一的作用是防止淘汰界面未响应）
    nothing=turtle.Turtle()
    nothing.hideturtle()
    #创建对象
    MyPen=turtle.Turtle()#蛇画笔（主画笔）
    Frame=turtle.Turtle()#边框画笔
    score=turtle.Turtle()#分数画笔
    food=turtle.Turtle()#食物画笔
    Hscore=turtle.Turtle()#最高分画笔
    Notice=turtle.Turtle()#通知画笔
    Special_food=turtle.Turtle()#特殊食物画笔
    #画笔预设（速度最快，隐藏画笔）
    MyPen.speed(0)
    Frame.speed(0)
    score.speed(0)
    food.speed(0)
    Hscore.speed(0)
    Notice.speed(0)
    Special_food.speed(0)
    MyPen.hideturtle()
    Frame.hideturtle()
    score.hideturtle()
    food.hideturtle()
    Hscore.hideturtle()
    Notice.hideturtle()
    Special_food.hideturtle()
    #蛇状态变量
    CoX={}
    CoY={}
    CoX_old={}
    CoY_old={}
    X_change={}
    Y_change={}
    #检验边框、食物大小和帧延迟预设合法性
    if Size%2 !=0 or Size%Dot_Diameter !=0 or frame_delay<0:#非法参数
        turtle.clearscreen()
        Notice.penup()
        Notice.goto(-200,100)
        screen.bgcolor("black")
        Notice.color("red")
        Notice.write("ERROR:ILLEGAL PARAMETER",font=("Arial",20,"bold"))
        Notice.goto(-20,-40)
        Notice.write(":(",font=("Arial",80,"normal"))
        start_time=time.time()
        stop_time=start_time+5#此处设置报错界面播放时长，此时为5秒
        while True:
            turtle.update()
            current_time=time.time()
            if current_time >= stop_time:
                break
        exit()
    def scene_draw():#绘制场景边框函数
        Frame.fillcolor(colors["scene_border"])
        Frame.pensize(1)
        size=Size
        Frame.begin_fill()
        Frame.penup()
        Frame.goto(-(size/2),size/2)
        Frame.pendown()
        Frame.goto(size/2,size/2)
        Frame.goto(size/2,-(size/2))
        Frame.goto(-(size/2),-(size/2))
        Frame.goto(-(size/2),size/2)
        Frame.end_fill()
        Frame.penup()
        Frame.goto((size/2)-50,-(size/2)-22)
        Frame.pendown()
        Frame.color("white")
        Frame.write("by QU QI",font=("Arial",10,"normal"))
    def draw(X,Y,color):#蛇绘制函数
        MyPen.color(color)
        MyPen.penup()
        MyPen.goto(X,Y)
        MyPen.pendown()
        MyPen.dot(Dot_Diameter)
    def draw_food(X,Y,color):#食物绘制函数
        food.color(color)
        food.penup()
        food.goto(X,Y)
        food.pendown()
        food.dot(Dot_Diameter)
    def draw_special_food(X,Y,color):#特殊食物绘制函数
        Special_food.color(color)
        Special_food.penup()
        Special_food.goto(X,Y)
        Special_food.pendown()
        Special_food.dot(Dot_Diameter)
    def draw_score():#分数打印函数
        score.color(colors["score"])
        score.penup()
        score.goto(int(Size/2)-100,int(Size/2)+25)
        score.pendown()
        score.write("Score:"+str(Score), font=("Arial",16,"normal"))
    def draw_highest_score():#最高分打印函数
        Hscore.color(colors["score"])
        Hscore.penup()
        Hscore.goto(int(Size/2)-100,int(Size/2)+6)
        Hscore.pendown()
        Hscore.write("Highest Score:"+str(real_highest_score), font=("Arial",16, "normal"))
    def food_generate(lower_boundary,upper_boundary):#食物生成函数
        no_repeat=0
        global foodX_permanent,foodY_permanent#全局声明
        while True:
            grid_lower = lower_boundary // Dot_Diameter#转换坐标为网格坐标
            grid_upper = upper_boundary // Dot_Diameter
            foodY_grid = random.randint(grid_lower, grid_upper)
            foodY = foodY_grid * Dot_Diameter#确保食物可被蛇碰到
            foodX_grid = random.randint(grid_lower, grid_upper)
            foodX = foodX_grid * Dot_Diameter
            for index8 in range(Dot_Number):#避免食物生成在蛇所在位置
                if foodX==CoX[index8] and foodY==CoY[index8]:
                    no_repeat=1
                    break
            if foodX>=int(Size/2) or foodX<=int(-Size/2) or foodY<=int(-Size/2) or foodY>=int(Size/2):#检查是否落在边框上或边框外
                no_repeat=1
            if no_repeat==0:
                break
            no_repeat=0  
        foodX_permanent=foodX
        foodY_permanent=foodY
    def special_food_generate(lower_boundary,upper_boundary):#特殊食物生成函数
        no_repeat2=0
        global special_foodX,special_foodY#全局声明
        while True:
            grid_lower = lower_boundary // Dot_Diameter#转换坐标为网格坐标
            grid_upper = upper_boundary // Dot_Diameter
            foodY_grid = random.randint(grid_lower, grid_upper)
            special_foodY = foodY_grid * Dot_Diameter#确保食物可被蛇碰到
            foodX_grid = random.randint(grid_lower, grid_upper)
            special_foodX = foodX_grid * Dot_Diameter
            for index8 in range(Dot_Number):#避免食物生成在蛇所在位置
                if special_foodX==CoX[index8] and special_foodY==CoY[index8]:
                    no_repeat2=1
                    break
            if special_foodX>=int(Size/2) or special_foodX<=int(-Size/2) or special_foodY<=int(-Size/2) or special_foodY>=int(Size/2):#检查是否落在边框上或边框外
                no_repeat2=1
            if special_foodX==foodX_permanent and special_foodY==foodY_permanent:#检查是否和普通食物重合
                no_repeat2=1
            if no_repeat2==0:
                break
    def special_food_timer():#特殊食物自动销毁函数
        global special_food_exist, special_food_start
        if special_food_exist==1:
            Current_time = time.time()
            if Current_time - special_food_start >= 15:#设置特殊食物自动销毁时长，当前为15秒
                special_food_exist = 0
                special_food_start = 0
                Special_food.clear()
            screen.ontimer(special_food_timer, 500)  
    def move_up():#蛇向上运动函数
        global direction_changed  # 引入全局变量
        if not direction_changed and Y_change[0] != -1:
            X_change[0]=0
            Y_change[0]=1
            direction_changed = True  # 标记方向已改变
    def move_down():#蛇向下运动函数
        global direction_changed
        if not direction_changed and Y_change[0] != 1:
            X_change[0]=0
            Y_change[0]=-1
            direction_changed = True
    def move_left():#蛇向左运动函数
        global direction_changed
        if not direction_changed and X_change[0] != 1:
            X_change[0]=-1
            Y_change[0]=0
            direction_changed = True
    def move_right():#蛇向右运动函数
        global direction_changed
        if not direction_changed and X_change[0] != -1:
            X_change[0]=1
            Y_change[0]=0
            direction_changed = True
    def end_game():#结束界面函数
        turtle.clearscreen()
        turtle.bgcolor(colors["end_screen_background"])#设置窗口背景颜色
        MyPen.penup()
        MyPen.goto(-160,100)
        MyPen.color(colors["GAME_OVER"])
        MyPen.write("GAME OVER", font=("Arial", 40, "bold"))
        MyPen.goto(0,60)
        MyPen.color(colors["end_screen_score"])
        MyPen.write("Score:"+str(Score), font=("Arial",30, "normal"),align="center")
        MyPen.goto(0,20)
        MyPen.write("Highest Score:"+str(real_highest_score), font=("Arial",30, "normal"),align="center")
        MyPen.goto(0,-10)
        MyPen.color(colors["PRESS_ENTER_TO_RESTART"])
        MyPen.write("[PRESS ENTER TO RESTART]", font=("Arial",15, "normal"),align="center")
        if highest_score<Score:#存取最新的最高分
            with open("highest_score.json","w") as HS2:
                    json.dump(real_highest_score,HS2)
    def pause():#暂停函数
        global is_pause
        if is_pause==0:
            Notice.pencolor(colors["pause"])
            Notice.penup()
            Notice.goto(0,0)
            Notice.write("PAUSE",font=("Arial",20, "normal"),align="center")
            is_pause=1
        else:
            is_pause=0
            Notice.clear()
            screen.ontimer(game_loop, int(frame_delay * 1000))
    #蛇初始化
    for index in range(initial_length):
        CoX[index]=0-Dot_Diameter*index
        CoY[index]=0
        X_change[index]=1
        Y_change[index]=0
    #初始化界面
    scene_draw()
    draw_score()
    draw_highest_score()
    #挂载运动函数到指定按键
    screen.onkeypress(move_up,up_setting)
    screen.onkeypress(move_down,down_setting)
    screen.onkeypress(move_left,left_setting)
    screen.onkeypress(move_right,right_setting)
    #挂载暂停函数至空格键
    screen.onkeypress(pause,"space")
    def game_loop():#游戏主循环
        global elimination,frame_delay,Score_change,Dot_Number,real_highest_score,Score,food_exist,foodX_permanent,foodY_permanent,Restart,initial_length,special_foodX,special_foodY,special_food_start,special_food_exist,score_change_number,direction_changed,is_pause,timer_id
        direction_changed = False#方向锁解锁
        #淘汰结束游戏
        if elimination==1:
            end_game()
            #判断是否重来
            while True:
                nothing.penup()#这三行代码没有实际意义，这是为了给turtle模块找点事做，防止窗口未响应^_^
                nothing.goto(1,0)
                nothing.goto(0,0)
                if keyboard.is_pressed("enter"):
                    Restart=1
                    break
            if Restart==1:#重来
                #恢复所有运行变量为默认值
                initial_length=3
                Dot_Number=initial_length
                food_exist=0
                special_food_exist=0
                foodX_permanent=0
                foodY_permanent=0
                Score=0
                Score_change=0
                elimination=0
                Restart=0
                special_foodX=0
                special_foodY=0
                score_change_number=0
                special_food_start=0
                _main_()
        if is_pause==0:#非暂停状态
            MyPen.clear()#清除旧画面
            if Score_change==1:
                draw_score()
                Score_change=0
            CoX_old=copy.copy(CoX)
            CoY_old=copy.copy(CoY)
            #得出刷新后的蛇头坐标
            CoX[0]=CoX[0]+X_change[0]*Dot_Diameter
            CoY[0]=CoY[0]+Y_change[0]*Dot_Diameter
            #蛇身跟随(上前补位)
            for index4 in range(1,Dot_Number):
                CoX[index4]=CoX_old[index4-1]
                CoY[index4]=CoY_old[index4-1]
            for index3 in range(Dot_Number):
                draw(CoX[index3],CoY[index3],colors["snake"])#根据坐标绘制蛇身
                #淘汰判断
                if CoX[0]==CoX[index3] and CoY[0]==CoY[index3] and 0 != index3:#咬到自身
                    elimination=1
                    break
                if CoX[0] <= -Size/2 or CoX[0] >= Size/2 or CoY[0] <= -Size/2 or CoY[0] >= Size/2:#撞到或越过边框
                    elimination=1
                    break
            #检测是否吃食
            if foodX_permanent==CoX[0] and foodY_permanent==CoY[0]:
                Score=Score+10
                #蛇身变长
                new_index = Dot_Number
                CoX[new_index] = CoX[new_index - 1]
                CoY[new_index] = CoY[new_index - 1]
                X_change[new_index] = X_change[new_index - 1]
                Y_change[new_index] = Y_change[new_index - 1]
                Dot_Number += 1
                #重绘分数与食物
                score.clear()
                Score_change=1
                food.clear()
                food_exist=0
                #计数
                score_change_number+=1
            #检测是否食用特殊食物
            if special_food_exist==1 and special_foodX == CoX[0] and special_foodY == CoY[0]:
                Score=Score+20
                score.clear()
                Score_change=1
                Special_food.clear()
                special_food_exist=0
                special_food_start=time.time()
            #特殊食物自动销毁
            special_food_timer()
            #刷新最高分
            if real_highest_score<Score:
                real_highest_score=Score
                Hscore.clear()
                draw_highest_score()
            #食物生成
            if food_exist==0:
                food_generate(int(-Size/2),int(Size/2))
                draw_food(foodX_permanent,foodY_permanent,colors["food"])
                food_exist=1
            #特殊食物生成
            if score_change_number==5 and special_food_exist==0:
                special_food_generate(int(-Size/2),int(Size/2))
                draw_special_food(special_foodX,special_foodY,colors["special_food"])
                special_food_exist=1
                score_change_number=0
                special_food_start=time.time()
            timer_id=screen.ontimer(game_loop, int(frame_delay * 1000))#递归下一次渲染(frame_delay秒后)
        screen.update()#屏幕刷新
    timer_id=screen.ontimer(game_loop, int(frame_delay * 1000))#启动游戏主循环并记录计时器ID
    turtle.done()
_main_()