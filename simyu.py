#フータオの初期パラメータは以下の通りです。
# レベル: 90
# HP: 15552
# 攻撃力: 106
# 護摩の杖の攻撃力: 608
# 会心率: 5%
# 会心ダメージ: 88.6%
Cha_HP = 15552
Cha_ATK = 106
staff_ATK = 608
base_CritRate = 0.05
base_CritDamage = 0.884
staff_CritDamage = 0.662
#よって基礎攻撃力は次の様になる
base_ATK = Cha_ATK + staff_ATK
#よって総合HPは次の様になる
#総合HP = (キャラHP * (1 + 時計のバフ値 + 護摩の杖のバフ + サブオプションの伸び) + 花固定値)
def total_HP(HPcount,switch):
    return (Cha_HP * (1 + 0.466 * (1-switch) + 0.200 + 0.058 * HPcount) + 4780)
#元素熟知の合計値を定義する
def total_EM(EMcount,switch):
    return (187 * switch + 23 * EMcount)
#また、総合攻撃力は次の様になる
#基礎攻撃力 = (キャラ攻撃力 + 武器固定値)
base_ATK = Cha_ATK + staff_ATK
#フータオの元素スキルの効果により、最大HPの6.26％が攻撃力に変換されます。
#また護摩の杖により、HP+20%。また、キャラクターのHP上限の0.8%分、攻撃力がアップする。キャラクターのHPが50%未満の時、攻撃力が更にHP上限の1%分アップする。
#よって、フータオのHPが50％未満と仮定して、合計攻撃力は天賦効果を考慮して以下の通りです。
#攻撃力＝基礎攻撃力 + 聖遺物固定値 + 総合体力 * (0.0626+0.008+0.01)
def atk(HPcount,switch):
    skill = total_HP(HPcount,switch) * 0.0626
    if skill > (base_ATK * 4):
        skill = base_ATK * 4
    return (base_ATK + 311 + total_HP(HPcount,switch) * (0.018) + skill)
#フータオのダメージボーナス％は以下の通りです。
#ダメージボーナス％ ＝ 杯の固定値 + 天賦効果HP50％以下の時に33％ + 火魔女4セット効果により炎元素ダメージ + 22.5％となります。
dmg_bonus = 0.466 + 0.33 + 0.225
#フータオの会心率は以下の通りです。
#会心率＝基礎会心率 + 聖遺物のメインオプション + 聖遺物のサブオプション
def total_CR(CRcount):
    cul = (base_CritRate + 0.311 + 0.039 * CRcount)
    if cul > 1:
        return 1
    else:
        return cul
#フータオの会心ダメージは以下の通りです。
#会心ダメージ＝基礎会心ダメージ + 聖遺物のサブオプション + 護摩の杖による会心ダメージ
def total_CD(CDcount):
    return (base_CritDamage + 0.078 * CDcount + 0.662)
#蒸発乗数% は以下の様に定義できる
#蒸発反応倍率 × ( 1 + 元素熟知の元素反応ダメージボーナス + 装備の効果)
#元素熟知の元素反応ダメージボーナスは以下の通りです。
#2.78*元素熟知 / (元素熟知+1400) 
def Vaporize_bonus(EMcount,switch):
    return (1.5 * (1 + 2.78 * total_EM(EMcount,switch) / (total_EM(EMcount,switch)+ 1400) + 0.15))
def calculate_damage(s, h, r, d, e):
    dmg_bonus = 0.466 + 0.33 + 0.225
    damage = atk(h, s) * 2.426 * (1 + dmg_bonus) * (1 + total_CR(r) * total_CD(d)) * 0.5 * 0.9 * Vaporize_bonus(e, s)
    return damage

def find_max_damage():
    max_damage = 0
    for s in range(0, 45):
        for h in range(0, 45):
            for r in range(0, 45):
                for d in range(0, 45):
                    e = 45 - h - r - d
                    if e < 0:
                        continue
                    damage = calculate_damage(s, h, r, d, e)
                    if damage > max_damage:
                        max_damage = damage
                        max_s = s
                        max_h = h
                        max_r = r
                        max_d = d
                        max_e = e
    return max_damage , max_s , max_h , max_r , max_d , max_e
max_damage, max_s, max_h, max_r, max_d, max_e = find_max_damage()
print("Max Damage:", max_damage)
if max_s == 1:
    print("熟知時計")
else:
    print("HP時計")
print("HP:", total_HP(max_h, max_s))
print("熟知:", total_EM(max_e, max_s))
print("会心:", total_CR(max_r))
print("会心ダメ:", total_CD(max_d))
print("HPサブオプ:", max_h)
print("熟知サブオプ:", max_e)
print("会心サブオプ:", max_r)
print("会心ダメサブオプ:", max_d)