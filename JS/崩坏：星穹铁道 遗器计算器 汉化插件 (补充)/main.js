// ==UserScript==
// @name         Fribbels 崩坏：星穹铁道 遗器计算器 汉化插件 (补充)
// @namespace    https://bbs.nga.cn/nuke.php?func=ucp&uid=41369816
// @license      MIT
// @version      1.0.4
// @description  翻译遗器计算器的基础UI说明。
// @author       浮砂, jkfujr
// @match        http*://fribbels.github.io/hsr-optimizer*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=github.io
// ==/UserScript==

(function () {
  "use strict";
  const i18n = new Map([
    /* Top Bar */
    ["Fribbels Honkai Star Rail Optimizer", "Fribbels的“崩坏：星穹铁道”优化器"],

    /* Left Bar */
    ["Optimization", "优化"],
    ["Optimizer", "优化器"],
    ["Characters", "角色"],
    ["Relics", "遗器"],
    ["Ornament", "饰品"],
    ["Ornaments", "饰品"],
    ["Import / Save", "导入 / 保存"],
    ["Settings", "设置"],
    ["Get Started", "教程"],
    ["Tools", "工具"],
    ["Relic Scorer", "遗器评分"],
    ["Changelog", "更新日志"],
    ["Links", "链接"],

    /* Common: Character */
    ["March 7th", "三月七"],
    ["March 7th (Hunt)", "三月七(巡猎)"],
    ["Dan Heng", "丹恒"],
    ["Himeko", "姬子"],
    ["Welt", "瓦尔特"],
    ["Kafka", "卡芙卡"],
    ["Silver Wolf", "银狼"],
    ["Arlan", "阿兰"],
    ["Asta", "艾丝妲"],
    ["Herta", "黑塔"],
    ["Bronya", "布洛妮娅"],
    ["Seele", "希儿"],
    ["Serval", "希露瓦"],
    ["Gepard", "杰帕德"],
    ["Natasha", "娜塔莎"],
    ["Pela", "佩拉"],
    ["Clara", "克拉拉"],
    ["Sampo", "桑博"],
    ["Hook", "虎克"],
    ["Lynx", "玲可"],
    ["Luka", "卢卡"],
    ["Topaz & Numby", "托帕&账账"],
    ["Qingque", "青雀"],
    ["Tingyun", "停云"],
    ["Luocha", "罗刹"],
    ["Jing Yuan", "景元"],
    ["Blade", "刃"],
    ["Sushang", "素裳"],
    ["Yukong", "驭空"],
    ["Fu Xuan", "符玄"],
    ["Yanqing", "彦卿"],
    ["Guinaifen", "桂乃芬"],
    ["Bailu", "白露"],
    ["Jingliu", "镜流"],
    ["Imbibitor Lunae", "丹恒•饮月"],
    ["Xueyi", "雪衣"],
    ["Hanya", "寒鸦"],
    ["Huohuo", "藿藿"],
    ["Gallagher", "加拉赫"],
    ["Argenti", "银枝"],
    ["Ruan Mei", "阮•梅"],
    ["Aventurine", "砂金"],
    ["Dr. Ratio", "真理医生"],
    ["Sparkle", "花火"],
    ["Black Swan", "黑天鹅"],
    ["Acheron", "黄泉"],
    ["Robin", "知更鸟"],
    ["Firefly", "流萤"],
    ["Misha", "米沙"],
    ["Jade", "翡翠"],
    ["Boothill", "波提欧"],
    ["Jiaoqiu", "椒丘"],
    ["Yunli", "云璃"],
    ["", ""],
    ["", ""],
    ["Caelus (Destruction)", "穹(毁灭)"],
    ["Caelus (Harmony)", "穹(同谐)"],
    ["Caelus (Preservation)", "穹(存护)"],
    ["Stelle (Destruction)", "星(毁灭)"],
    ["Stelle (Harmony)", "星(同谐)"],
    ["Stelle (Preservation)", "星(存护)"],

    /* Main: Optimizer */
    ["Character options", "角色选项"],
    ["Character", "角色"],

    ["Light cone", "光锥"],
    ["Presets", "预设"],
    ["Recommended presets", "推荐的预设集"],
    ["Optimization target", "优化目标"],
    ["Find top results", "查找前?个结果"],
    ["Find top 100 results", "查找前100个结果"],
    ["Find top 1,000 results", "查找前1,000个结果"],
    ["Find top 10,000 results", "查找前10,000个结果"],
    ["Find top 100,000 results", "查找前100,000个结果"],
    ["Find top 1,000,000 results", "查找前1,000,000个结果"],
    ["Sorted by", "根据?排序"],
    ["Damage calculations", "伤害计算"],
    ["Sorted by Basic DMG", "根据普攻伤害排序"],
    ["Sorted by Skill DMG", "根据战技伤害排序"],
    ["Sorted by Ult DMG", "根据终结技伤害排序"],
    ["Sorted by Follow-up DMG", "根据追加攻击伤害排序"],
    ["Sorted by DoT DMG", "根据持续伤害排序"],
    ["Sorted by Break DMG", "根据击破伤害排序"],
    ["Computed ratings", "计算评级"],
    ["Sorted by Weight", "根据权重排序"],
    ["Sorted by Effective HP", "根据有效生命值排序"],
    ["Stats", "属性"],
    ["Sorted by HP", "根据生命值排序"],
    ["Sorted by ATK", "根据攻击力排序"],
    ["Sorted by DEF", "根据防御力排序"],
    ["Sorted by SPD", "根据速度排序"],
    ["Sorted by CRIT Rate", "根据暴击率排序"],
    ["Sorted by CRIT DMG", "根据暴击伤害排序"],
    ["Sorted by Effect HIT", "根据效果命中排序"],
    ["Sorted by Effect RES", "根据效果抵抗排序"],
    ["Sorted by Break Effect", "根据击破特攻排序"],
    ["Sorted by Healing Boost", "根据治疗量加成排序"],
    ["Sorted by Energy Regen", "根据能量恢复效率排序"],
    ["Sorted by Elemental DMG", "根据属性伤害加成排序"],
    ["Character passives", "角色被动"],
    ["Light cone passives", "光锥被动"],
    ["Enemy options", "敌方选项"],
    ["Elemental weakness", "具备该属性的弱点"],
    ["Weakness broken", "正处于弱点击破状态"],
    ["Optimizer options", "优化选项"],
    ["Maxed main stat", "统计最大主属性"],
    ["Allow equipped relics", "计入已被装备的遗器"],
    ["Character priority filter", "角色优先级筛选"],
    ["Keep current relics", "保留当前遗器"],
    ["Priority", "优先级"],
    ["Exclude", "排除"],
    ["Relic enhance / rarity", "遗器强化/稀有度"],
    ["Relic & stat filters", "遗器&属性筛选"],
    ["STAT\nWEIGHT", "属性\n权重"],
    ["BASIC\nDMG", "基础\n伤害"],
    ["SKILL\nDMG", "技能\n伤害"],
    ["ULT\nDMG", "终结技\n伤害"],
    ["FUA\nDMG", "追加攻击\n伤害"],
    ["DOT\nDMG", "持续伤害\n伤害"],
    ["BREAK\nDMG", "击破\n伤害"],
    ["COMBO\nDMG", "组合技\n伤害"],
    [["Main stats", "Main\nStat", "Main stat"], "主属性"],
    ["Head", "头部"],
    ["Hands", "手部"],
    ["Body", "身体"],
    ["Feet", "脚部"],
    ["Sphere", "球"],
    ["Rope", "绳"],
    ["Planar Sphere", "位面球"],
    [["Link Rope", "Link rope"], "连结绳"],
    ["Sets", "套装"],
    ["Relic set", "遗器套装"],
    ["Ornament set", "饰品套装"],
    ["HP%", "生命百分比"],
    ["ATK%", "攻击百分比"],
    ["DEF%", "防御百分比"],
    ["CRIT Rate", "暴击率"],
    ["CRIT DMG", "暴击伤害"],
    [["HIT", "Effect HIT Rate"], "效果命中"],
    [
      [
        "Healing",
        "Healing Boost",
        "Outgoing Healing",
        "Outgoing Healing Boost",
      ],
      "治疗量加成",
    ],
    ["HEAL", "治疗"],
    ["Speed", "速度"],
    ["Physical DMG", "物理属性伤害"],
    ["Fire DMG", "火属性伤害"],
    ["Ice DMG", "冰属性伤害"],
    ["Lightning DMG", "雷属性伤害"],
    ["Wind DMG", "风属性伤害"],
    ["Quantum DMG", "量子属性伤害"],
    ["Imaginary DMG", "虚数属性伤害"],
    ["Physical", "物理"],
    ["Fire", "火"],
    ["Ice", "冰"],
    ["Lightning", "雷"],
    ["Wind", "风"],
    ["Quantum", "量子"],
    ["Imaginary", "虚数"],
    [["Energy Regen", "Energy Regeneration Rate"], "能量恢复效率"],
    ["Energy", "能量"],
    ["Conditional set effects", "条件：套装效果"],
    ["Substat weight filter", "副属性权重过滤"],
    ["Min weighted rolls per relic", "遗器的最低加权词条数量"],
    ["HP", "生命值"],
    ["ATK", "攻击力"],
    ["DEF", "防御力"],
    ["SPD", "速度"],
    ["CR", "暴击率"],
    ["CD", "暴伤"],
    ["EHR", "命中"],
    ["RES", "抵抗"],
    ["BE", "击破"],
    ["ERR", "充能效率"],
    // Σ CR
    ["Σ HP", "Σ 生命"],
    ["Σ ATK", "Σ 攻击"],
    ["Σ DEF", "Σ 防御"],
    ["Σ SPD", "Σ 速度"],
    ["Σ CR", "Σ 暴击"],
    ["Σ CD", "Σ 暴伤"],
    ["Σ EHR", "Σ 命中"],
    ["Σ RES", "Σ 抵抗"],
    ["Σ BE", "Σ 击破"],
    ["Σ ERR", "Σ 充能"],
    ["Σ DMG", "Σ 伤害"],
    ["Page Size:", "每页数据量："],
    ["WEIGHT", "权重"],
    ["EHP", "有效生命"],
    ["BASIC", "普攻"],
    ["SKILL", "战技"],
    ["ULT", "终结技"],
    ["FUA", "追加攻击"],
    ["DOT", "持续伤害"],
    [["BREAK", "Break"], "击破伤害"],
    ["COMBO", "组合"],
    ["Break Effect", "击破特攻"],
    ["Stat filters", "属性过滤"],
    [["Effect HIT", "Effect Hit Rate"], "效果命中"],
    ["Effect RES", "效果抵抗"],
    ["Rating filters", "评分过滤"],
    ["Rotation COMBO formula", "旋转组合公式"],
    ["Basic DMG", "普攻伤害"],
    ["Skill DMG", "战技伤害"],
    ["Ult DMG", "终结技伤害"],
    ["Fua DMG", "追加攻击伤害"],
    ["Dot DMG", "持续伤害"],
    ["Break DMG", "击破伤害"],
    ["Additional options", "额外选项"],
    ["Extra combat buffs", "额外战斗buff"],
    //['', ''],
    ["Combat buffs", "战斗buffs"],
    ["HP %", "生命值百分比"],
    ["ATK %", "攻击力百分比"],
    ["DEF %", "防御力百分比"],
    ["Crit Rate %", "暴击率百分比"],
    ["Crit Dmg %", "暴击伤害百分比"],
    ["Crit DMG %", "暴击伤害百分比"],
    ["SPD %", "速度百分比"],
    ["BE %", "击破特攻百分比"],
    ["Dmg Boost %", "伤害加成百分比"],
    ["Teammates", "队友"],
    ["Character custom stats simulation", "角色自定义属性模拟"],
    ["Simulate builds", "模拟构筑"],
    ["Import optimizer build", "导入优化器构筑"],
    ["Off", "关闭"],
    ["Simulate custom substat rolls", "模拟自定义副属性随机"],
    ["Simulate custom substat totals", "模拟自定义副属性总计"],
    ["Options", "选项"],
    ["Substat value totals", "副属性值总计"],
    ["No custom simulations selected", "还未选择任何自定义模拟"],
    ["Simulation name (Optional)", "模拟名称(可选)"],
    ["Permutations", "排列"],
    ["Perms", "排列"],
    ["Searched", "已搜索"],
    ["Results", "结果"],
    ["Progress", "进度"],
    ["Controls", "控制"],
    ["Start optimizer", "开始优化"],
    ["Cancel", "取消"],
    ["Reset", "重设"],
    ["Stat and filter view", "属性和筛选的视图"],
    ["Basic stats", "基本属性"],
    ["Combat stats", "战斗属性"],
    ["Filter", "筛选"],
    ["Equip", "装备"],

    /* Main: 遗器 */
    ["Equipped by", "装备中"],
    ["Enhance / Grade", "强化 / 稀有度"],
    ["Substat upgrades", "副属性升级"],
    ["", ""],
    ["", ""],
    ["", ""],
    /* Main: 遗器 / Verified */
    ["Verified", "已验证"],
    [
      "Relic substats verified by relic scorer (speed decimals)",
      "通过遗器评分器验证的遗器副属性（速度小数点）",
    ],
    /* Main: 遗器 / Clear */
    ["Clear", "清除"],
    ["Clear all filters", "清除所有筛选条件"],
    /* Main: 遗器 / Set */
    ["Set", "套装"],
    ["Passerby of Wandering Cloud", "云无留迹的过客"],
    ["Musketeer of Wild Wheat", "野穗伴行的快枪手"],
    ["Knight of Purity Palace", "净庭教宗的圣骑士"],
    ["Hunter of Glacial Forest", "密林卧雪的猎人"],
    ["Champion of Streetwise Boxing", "街头出身的拳王"],
    ["Guard of Wuthering Snow", "戍卫风雪的铁卫"],
    ["Firesmith of Lava-Forging", "熔岩锻铸的火匠"],
    ["Genius of Brilliant Stars", "繁星璀璨的天才"],
    ["Band of Sizzling Thunder", "激奏雷电的乐队"],
    ["Eagle of Twilight Line", "晨昏交界的翔鹰"],
    ["Thief of Shooting Meteor", "流星追迹的怪盗"],
    ["Wastelander of Banditry Desert", "盗匪荒漠的废土客"],
    ["Longevous Disciple", "宝命长存的莳者"],
    ["Messenger Traversing Hackerspace", "骇域漫游的信使"],
    ["The Ashblazing Grand Duke", "毁烬焚骨的大公"],
    ["Prisoner in Deep Confinement", "幽锁深牢的系囚"],
    ["Pioneer Diver of Dead Waters", "死水深潜的先驱"],
    ["Watchmaker, Master of Dream Machinations", "机心戏梦的钟表匠"],
    ["Iron Cavalry Against the Scourge", "荡除蠹灾的铁骑"],
    ["The Wind-Soaring Valorous", "风举云飞的勇烈"],
    ["Space Sealing Station", "太空封印站"],
    ["Fleet of the Ageless", "不老者的仙舟"],
    ["Pan-Cosmic Commercial Enterprise", "泛银河商业公司"],
    ["Belobog of the Architects", "筑城者的贝洛伯格"],
    ["Celestial Differentiator", "星体差分机"],
    ["Inert Salsotto", "停转的萨尔索图"],
    ["Talia: Kingdom of Banditry", "盗贼公国塔利亚"],
    ["Sprightly Vonwacq", "生命的翁瓦克"],
    ["Rutilant Arena", "繁星竞技场"],
    ["Broken Keel", "折断的龙骨"],
    ["Firmament Frontline: Glamoth", "苍穹战线格拉默"],
    ["Penacony, Land of the Dreams", "梦想之地匹诺康尼"],
    ["Sigonia, the Unclaimed Desolation", "无主荒星茨冈尼亚"],
    ["Izumo Gensei and Takama Divine Realm", "出云显世与高天神国"],
    ["Duran, Dynasty of Running Wolves", "奔狼的都蓝王朝"],
    ["Forge of the Kalpagni Lantern", "劫火莲灯铸炼宫"],
    ["", ""],
    ["", ""],
    ["", ""],
    ["", ""],
    /* Main: 遗器 / MainStat */
    ["Physical DMG Boost", "物理属性伤害提高"],
    ["Fire DMG Boost", "火属性伤害提高"],
    ["Ice DMG Boost", "冰属性伤害提高"],
    ["Lightning DMG Boost", "雷属性伤害提高"],
    ["Wind DMG Boost", "风属性伤害提高"],
    ["Quantum DMG Boost", "量子属性伤害提高"],
    ["Imaginary DMG Boost", "虚数属性伤害提高"],
    /* Main: 遗器 / Substats */
    ["Substats", "副属性"],
    /* Main: 遗器 / Relic recommendation characte */
    ["Relic recommendation character", "遗器推荐角色"],
    ["Reapply scores", "重新计算分数"],
    ["Scoring algorithm", "评分算法"],
    ["Stat weights", "属性权重"],
    ["Optimal main stats", "最佳主属性"],
    ["Calculations", "计算"],

    /* Main: 遗器 / Relic recommendation characte / Tips */
    ["Click to show details", "点击显示详情"],
    ["Substat scoring is calculated by", "副属性评分计算方法"],
    ["Score = weight * normalization * value", "评分 = 权重 * 规范化 * 值"],
    [
      ". The weight of each stat is defined above, on a scale of 0 to 1. The normalization of each stat is calculated based on the ratio of their main stat values to Crit DMG with max value",
      ". 每个属性的权重如上所述，范围为0到1。每个属性的规范化是根据其主属性值与暴击伤害最大值的比率计算的",
    ],
    ["CD BE = 64.8 / 64.8 == 1.0", "暴击伤害 = 64.8 / 64.8 == 1.0"],
    ["SPD = 64.8 / 25.032 == 2.59", "速度 = 64.8 / 25.032 == 2.59"],
    ["DEF% = 64.8 / 54.0 == 1.2", "防御百分比 = 64.8 / 54.0 == 1.2"],
    ["OHB = 64.8 / 34.561 == 1.87", "生命值百分比 = 64.8 / 34.561 == 1.87"],
    [
      "HP% ATK% EHR RES = 64.8 / 43.2 == 1.5",
      "生命百分比 攻击百分比 效果命中 抵抗 = 64.8 / 43.2 == 1.5",
    ],
    ["ERR = 64.8 / 19.439 == 3.33", "能量恢复 = 64.8 / 19.439 == 3.33"],
    ["CR = 64.8 / 32.4 == 2", "暴击率 = 64.8 / 32.4 == 2"],
    ["ELEMENTAL DMG = 64.8 / 38.88 == 1.67", "元素伤害 = 64.8 / 38.88 == 1.67"],
    [
      "Flat ATK/HP/DEF have a separate calculation:",
      "平A/生命/防御有单独的计算: ",
    ],
    [
      "1 / (2 * character base * 0.01) * (64.8 / (% main stat value))",
      "1 / (2 * 角色基础值 * 0.01) * (64.8 / (% 主属性值))",
    ],
    [
      ". This converts the flat stat value to a percent equivalent by base stats, then normalizes it. Double the character base is used instead of character + light cone base due to the variable nature of light cone stats.",
      "。这将平面属性值转换为基础属性的百分比等效值，然后将其规范化。使用角色基础值的两倍，而不是角色 + 光锥基础值，是因为光锥属性的可变性。",
    ],
    [
      "A letter grade is assigned based on the number of normalized min rolls of each substat. The score for each min roll in theory should be equivalent to",
      "根据每个副属性的规范化最小投掷次数分配字母等级。理论上每个最小投掷的得分应等于",
    ],
    [
      ", but is rounded down to",
      ", 但由于游戏不显示额外的小数位，得分向下舍入为",
    ],
    [
      "due to the game not displaying extra decimals. The general scale for grade by rolls is",
      "。投掷次数的等级一般为",
    ],
    ["with a", "使用"],
    ["assigned for an additional half roll.", "分配额外的半次投掷。"],
    ["Character scores are calculated by", "角色评分的计算方式为"],
    [
      "Score = sum(relic substat scores) + sum(main stat scores)",
      "评分 = 遗器副属性评分之和 + 主属性评分之和",
    ],
    [
      ". Only the feet/body/sphere/rope relics have main stat scores. The main stat score for a 5 star maxed relic is",
      ". 只有脚部、身体、位面球和连结绳遗器具有主属性评分。五星满级遗器的主属性评分为",
    ],
    [
      "if the main stat is optimal, otherwise scaled down by the stat weight. Non 5 star relic scores are also scaled down by their maximum enhance. Characters are expected to have 3 full sets, so 3 rolls worth of score is deducted for each missing set.",
      "如果主属性是最优的，否则按属性权重缩减。非五星遗器的评分也会按其最大强化等级缩减。角色预计会有3个完整套装，因此每缺少一个套装会扣除相当于3次投掷的评分。",
    ],
    [
      "Body/feet/sphere/rope relics are granted extra rolls to compensate for the difficulty of obtaining optimal main stats with desired substats. These numbers were calculated by a simulation of relic rolls accounting for main stat drop rate and expected substat value. These rolls are multiplied by the min roll value of",
      "为了补偿在获得最优主属性和所需副属性的难度，身体、脚部、位面球和连结绳遗器会获得额外的投掷次数。这些数值是通过模拟遗器投掷并考虑主属性掉落率和预期副属性值计算得出的。这些投掷次数乘以最小投掷值",
    ],
    ["for the bonus score value.", "来计算额外的评分值。"],
    ["Body HP_P 1.320", "身体 生命值百分比 1.320"],
    ["Body ATK_P 1.284", "身体 攻击力百分比 1.284"],
    ["Body DEF_P 1.305", "身体 防御力百分比 1.305"],
    ["Body CR 1.644", "身体 暴击率 1.644"],
    ["Body CD 1.658", "身体 暴击伤害 1.658"],
    ["Body OHB 1.712", "身体 生命值百分比 1.712"],
    ["Body EHR 1.668", "身体 效果命中 1.668"],
    ["Feet HP_P 1.058", "脚部 生命值百分比 1.058"],
    ["Feet ATK_P 1.019", "脚部 攻击力百分比 1.019"],
    ["Feet DEF_P 1.000", "脚部 防御力百分比 1.000"],
    ["Feet SPD 1.567", "脚部 速度 1.567"],
    ["PlanarSphere HP_P 1.583", "位面球 生命值百分比 1.583"],
    ["PlanarSphere ATK_P 1.559", "位面球 攻击力百分比 1.559"],
    ["PlanarSphere DEF_P 1.587", "位面球 防御力百分比 1.587"],
    ["PlanarSphere ELEM 1.763", "位面球 元素伤害 1.763"],
    ["LinkRope HP_P 1.073", "连结绳 生命值百分比 1.073"],
    ["LinkRope ATK_P 1.076", "连结绳 攻击力百分比 1.076"],
    ["LinkRope DEF_P 1.172", "连结绳 防御力百分比 1.172"],
    ["LinkRope BE 1.416", "连结绳 击破效果 1.416"],
    ["LinkRope ERR 2.000", "连结绳 能量恢复 2.000"],
    [
      "This scoring method is still experimental and subject to change, please come by the discord server to share any feedback!",
      "这种评分方法仍在试验中，可能会有所变化，请加入我们的Discord服务器分享您的反馈！",
    ],
    ["Reset to default", "恢复默认"],
    ["Reset all characters", "重置所有角色"],
    ["Save changes", "保存更改"],

    /* Main: 遗器 / Relic ratings */
    ["Relic ratings", "遗器评分"],
    ["Selected character", "选定角色"],
    ["Selected character: Score", "选定角色: 分数"],
    ["Selected character: Average potential", "选定角色: 平均潜力"],
    ["Selected character: Max potential", "选定角色: 最大潜力"],
    ["Custom characters", "自定义角色"],
    ["Custom characters: Avg potential", "自定义角色: 平均潜力"],
    ["Custom characters: Max potential", "自定义角色: 最大潜力"],
    ["All characters", "所有角色"],
    ["All characters: Avg potential", "所有角色: 平均潜力"],
    ["All characters: Max potential", "所有角色: 最大潜力"],
    ["Coming soon", "即将发布"],
    ["Relic / Ornament sets potential", "遗器/饰品潜力"],
    ["", ""],
    ["", ""],

    /* Main: 遗器 / Relic ratings / Tips */
    ["Value Columns", "价值列"],
    [
      "You can optionally display a number of columns that assess the relative 'value' of a relic.",
      "您可以选择显示多个列，以评估遗器的相对“价值”。",
    ],
    ["Weight", "权重"],
    [
      "Weight columns assess the contribution of a particular relic to the overall letter grading of the selected recommendation character (if any).",
      "权重列评估特定遗器对所选推荐角色（如果有）的整体字母评分的贡献。",
    ],
    [
      "Weight can show the current value of a relic, the possible best case upgraded weight, or an 'average' weight that you're more likely to see",
      "权重可以显示当前遗器的价值、可能的最佳升级权重或更可能出现的“平均”权重。",
    ],
    [
      "Weight is useful to focus on a single character and see which relics might give them a higher letter grading.",
      "权重对于专注于单个角色并查看哪些遗器可能提高他们的字母评分非常有用。",
    ],
    ["Potential", "潜力"],
    [
      "Potential is a character-specific percentage of how good the relic could be (or 'is', if fully upgraded), compared against the stats on a fully upgraded 'perfect' relic in that slot.",
      "潜力是角色特定的百分比，用于衡量遗器（如果完全升级）有多好，与该位置上完全升级的“完美”遗器的统计数据进行对比。",
    ],
    [
      "Potential can look at all characters or just owned. It then takes the maximum percentage for any character.",
      "潜力可以查看所有角色或仅查看已拥有的角色，然后取任何角色的最大百分比。",
    ],
    [
      "Potential is useful for finding relics that aren't good on any character, or hidden gems that could be great when upgraded.",
      "潜力对于找到对任何角色都不好的遗器或在升级后可能非常出色的隐藏宝石非常有用。",
    ],
    [
      "Note ordering by potential can be mismatched against weights, due to weight calculations preferring lower weight ideal mainstats.",
      "注意，由于权重计算偏好较低权重的理想主属性，因此按潜力排序可能与权重不一致。",
    ],

    /* Main: 遗器 / Custom potential characters */
    ["Custom potential characters", "自定义潜力角色"],
    ["Customize characters", "自定义角色"],
    ["All characters enabled", "已启用所有角色"],
    [/^(\d+) characters excluded$/, "$1 已排除的角色"],
    ["Select characters to exclude", "选择要排除的角色"],
    ["Search character name", "搜索角色名称"],
    ["Exclude all", "全部排除"],

    /* Main: 遗器 / Relic Grid */
    ["Owner", "装备中"],
    ["Grade", "稀有度"],
    ["Enhance", "等级"],
    ["Part", "部位"],
    ["Main Value", "主属性\n值"],
    ["Crit\nRate", "暴击率"],
    ["Crit\nDMG", "暴击伤害"],
    ["Effect\nHit Rate", "效果命中"],
    ["Effect\nRES", "效果抵抗"],
    ["Break\nEffect", "击破效果"],
    ["Crit\nValue", "暴击\n值"],
    ["Selected Char\nScore", "已选角色\n评分"],
    ["Selected Char\nAvg Potential", "已选角色\n平均潜力"],
    ["Selected Char\nMax Potential", "已选角色\n最大潜力"],
    ["Custom Chars\nAvg Potential", "自定义角色\n平均潜力"],
    ["Custom Chars\nMax Potential", "自定义角色\n最大潜力"],

    ["Edit Relic", "编辑遗器"],
    ["Add New Relic", "添加新遗器"],
    ["Delete Relic", "删除遗器"],
    ["Delete this relic?", "删除这个遗器？"],
    ["Confirm", "确认"],
    ["Submit", "提交"],
    ["Show custom characters", "显示自定义角色"],
    ["Show all characters", "显示所有角色"],
    /* Main: 遗器 / Relic Grid / Relic Insight */
    ["Relic Insight: Buckets", "遗器分析：分类"],
    ["Relic Insight: Top 10", "遗器分析：前十"],

    /* Main: 遗器 / Relic Grid / Relic Insight / Tips-1 */

    ["Relic Insight", "遗器分析"],
    [
      "When a relic is selected in the table above, you can choose an analysis to view a plot of.",
      "当您在上表中选择一个遗器时，您可以选择一种分析来查看其图表。",
    ],
    [
      "'Buckets' looks at how perfect this relic could be (with the best possible upgrade rolls) for each character, and buckets them into percentages.",
      "'分类'分析查看该遗器对每个角色可能达到的完美程度（使用最佳升级结果），并将其按百分比分类。",
    ],
    [
      "If you hover over a character portrait you'll see the new stats and/or rolls necessary to reach the max potential of this relic.",
      "如果您将鼠标悬停在角色肖像上，您将看到达到该遗器最大潜力所需的新属性和/或结果。",
    ],
    [
      "⚠️ Relics with missing substats may have misleadlingly high buckets, as best-case upgrade analysis assumes the best new substat per character.",
      "⚠️ 缺少副属性的遗器可能会有误导性高的分类，因为最佳升级分析假设每个角色都有最佳新副属性。",
    ],
    [
      "'Top 10' takes the top 10 characters that this relic could be best for, and shows the range of '% perfection' upgrading this relic could result in.",
      "'前十'分析列出该遗器最适合的前十个角色，并显示升级该遗器可能达到的“完美百分比”范围。",
    ],

    /* Main: 遗器 / Relic Grid / Relic Insight / Tips-2 */
    [
      "Note - Potential is a percent rating which compares a relic to the best possible +15 relic for the current character in the slot. This rating is based off the scoring algorithm weights. This means unrolled relics at +0 sometimes have a higher potential than existing +15 relics, because their possible rolls can go into the character's desired stats.",
      "注意 - 潜力是一个百分比评级，将遗器与当前角色在该位置上最佳可能的+15遗器进行比较。该评级基于评分算法的权重。这意味着未升级的+0遗器有时比现有的+15遗器具有更高的潜力，因为它们可能的升级结果可以进入角色所需的属性。",
    ],
    [
      "Selected character: Score - The relic's current weight as defined by the scoring algorithm for the currently selected character",
      "已选角色：评分 - 根据评分算法定义的当前已选角色的遗器当前权重",
    ],
    [
      "Selected character: Average potential - The relic's potential weight if rolls went into the average weight of the relic's substats",
      "已选角色：平均潜力 - 如果升级结果进入遗器副属性的平均权重，则遗器的潜在权重",
    ],
    [
      "Selected character: Max potential - The relic's maximum potential weight if all future rolls went into the character's desired stats",
      "已选角色：最大潜力 - 如果所有未来的升级结果都进入角色所需的属性，则遗器的最大潜在权重",
    ],
    [
      "All characters: Max potential - The highest possible potential value of the relic, out of all characters in the game.",
      "所有角色：最大潜力 - 游戏中所有角色中遗器的最高可能潜在值。",
    ],

    /* Main: 设置 */
    ["Equipping relics from another character", "从其他角色装备遗器"],
    ["Swap relics with previous owner", "与前一个拥有者交换遗器"],
    ["Replace relics without swapping", "替换遗器而不进行交换"],
    [
      "Move Optimizer sidebar to the bottom on smaller screens",
      "在小屏幕上将侧边栏移到底部",
    ],
    ["No, always keep the sidebar on the right", "总是保持在右侧"],
    [
      "Show on bottom only at the smallest possible screen size",
      "仅在小屏幕下显示在底部",
    ],
    ["Show on bottom for best-looking layout", "为了最佳布局效果显示在底部"],

    /* Main: 导入 / Save */
    ["Relic scanner importer", "遗器扫描导入"],
    [
      "Install and run one of the relic scanner options:",
      "安装并运行以下遗器扫描选项之一：",
    ],
    [
      "(Recommended) IceDynamix Reliquary Archiver",
      "(推荐) IceDynamix Reliquary Archiver",
    ],
    ["Accurate speed decimals, instant scan", "迅速的扫描，提供精确的速度小数"],
    ["Imports full inventory and character roster", "导入完整的库存和角色名单"],
    [
      "Inaccurate speed decimals, 5-10 minutes OCR scan",
      "5-10分钟的OCR扫描，提供不准确的速度小数",
    ],
    [
      "Inaccurate speed decimals, instant scan",
      "迅速的扫描，提供不准确的速度小数",
    ],
    [
      "No download needed, but limited to relics from the 8 characters on profile showcase",
      "无需下载，但只能获取到角色展柜中角色的遗器",
    ],
    [
      "No download needed, but limited to ingame characters' equipped relics",
      "无需下载，但只能获取到游戏内角色的遗器",
    ],
    ["Upload scanner json file", "上传扫描获取的json文件"],
    ["or", "或"],
    ["Paste json file contents", "在这里粘贴json文件的内容"],
    ["Import relics", "导入遗器"],
    ["Import relics & characters", "导入遗器和角色"],
    [
      "Import relics only. Updates the optimizer with the new dataset of relics and doesn't overwrite builds.",
      "仅导入遗器。使用新的遗器数据集来更新优化器，不会覆盖已有构筑。",
    ],
    ["OR", "或者"],
    [
      "Import relics and characters. Replaces the optimizer builds with ingame builds.",
      "导入遗器和角色。使用游戏内的已装备套装来覆盖优化器的已有构筑。",
    ],
    ["Overwrite optimizer builds", "覆盖优化器的构筑"],
    [
      "Are you sure you want to overwrite your optimizer builds with ingame builds?",
      "你确定要用游戏内的已装备套装来覆盖优化器的已有构筑吗?",
    ],
    ["Yes", "是"],
    ["", ""],
    ["", ""],
    ["", ""],
    ["", ""],
    ["Load optimizer data", "读取优化器数据"],
    [
      "Load your optimizer data from a file.",
      "从特定文件中读取您的优化器数据。",
    ],
    ["Load save data", "读取保存的数据"],
    [
      "Invalid save file, please try a different file. Did you mean to use Relic Importer tab?",
      "无效的保存文件，请尝试其他文件。或者您其实需要前往遗器导入页面？",
    ],
    ["Done!", "成功！"],
    ["Save optimizer data", "保存优化器数据"],
    [
      "Save your optimizer data to a file.",
      "将您的优化器数据保存到一个文件里。",
    ],
    ["Save data", "保存数据"],
    ["Clear optimizer data", "清除优化器数据"],
    ["Clear all optimizer data.", "清除所有的优化器数据。"],
    ["Clear data", "清除数据"],

    /* Modal: Select Character*/
    ["Select a character", "选择一个角色"],
    ["Search character name", "搜索角色名称"],

    /* Modal: Select Lightcone*/
    ["Select a light cone", "选择一个光锥"],

    /* Popup: Suit */
    ["4 Piece", "四件套"],
    ["2 + 2 Piece", "2组二件套"],
    ["2 + Any", "1组二件套"],

    /* Tips */
    [
      "Select the character and eidolon. Character is assumed to be level 80 with maxed traces in optimization calcs.",
      "选择角色与星魂等级(右侧E几)。在模拟计算中，角色默认为80级且满行迹。",
    ],
    [
      "Select the light cone and superimposition. Light cone is assumed to be level 80 in optimization calcs.",
      "选择光锥与叠影等级(右侧S几)。在模拟计算中，光锥默认为80级。",
    ],
    [
      "Superimposition and passive effects are applied under the Light cone passives panel.",
      '叠影效果和光锥被动效果均会应用于"光锥被动"栏目。',
    ],
    [
      "Select the conditional effects to apply to the character.",
      "选择要应用于角色的状态效果。",
    ],
    [
      "Effects that rely on combat stats or environment state will be applied by default, so only the options that require user input are listed here.",
      "默认情况下，将应用依赖于战斗统计数据或环境状态的效果，因此此处仅列出需要您选择的选项。",
    ],
    [
      "Select the conditional effects to apply to the light cone.",
      "选择要应用于光锥的状态效果。",
    ],
    [
      "Level - Enemy level, affects enemy DEF calculations",
      "等级(Level) - 敌人的等级，会影响其防御力的计算",
    ],
    [
      "Targets - Number of targets in the battle. The target enemy is always assumed to be in the center, and damage calculations are only for the single primary target.",
      "目标(Targets) - 战斗中的目标数量。目标敌人总是被假设在中心，并且伤害计算仅针对单个主要目标。",
    ],
    [
      `RES - Enemy elemental RES. RES is set to 0 when the enemy's elemental weakness is enabled.`,
      '抗性(RES) - 敌人对选定角色所属属性的抗性。当"具备该属性的弱点"选项激活时抗性将被设为0。',
    ],
    [
      `Max toughness - Enemy's maximum toughness bar value. Affects calculations related to break damage.`,
      "最大韧性(Max toughness) - 敌人的最大韧性条值。影响与击破伤害相关的计算。",
    ],
    [
      `Elemental weakness - Whether the enemy is weak to the character's type. Enabling this sets enemy elemental RES % to 0.`,
      "具备该属性的弱点(Elemental weakness) - 敌人是否具备角色所属属性的弱点。激活此项时会将其抗性设为0。",
    ],
    [
      `Weakness broken - Whether the enemy's toughness bar is broken. Affects damage calculations and certain character passives.`,
      "正处于弱点击破状态(Weakness broken) - 敌人的韧性条是否已被击破。影响伤害计算和某些角色的被动效果。",
    ],
    [
      `Select main stats to use for optimization search. Multiple values can be selected for more options`,
      "选择主属性以供优化器检索。通过更多选项可以选择多个筛选项。",
    ],
    [
      `Select the relic and ornament sets to filter results by. Multiple sets can be selected for more options`,
      "选择要过滤的遗器/位面饰品套装。通过更多选项可以选择多个筛选项。",
    ],
    [
      `Set effects will be accounted for in calculations, use the Conditional set effects menu to customize which effects are active.`,
      "套装效果将在优化中被计入，使用“条件：套装效果”菜单自定义哪些效果会被激活。",
    ],
    [
      `This filter is used to reduce the number of permutations the optimizer has to process.`,
      "该过滤器用于减少优化器需要处理的排列次数。",
    ],
    [
      `It works by first scoring each relic per slot by the weights defined, then filtering by the number of weighted min rolls the relic has.`,
      "它的工作原理是，首先根据定义的权重对每个位置的遗器进行评分，然后根据加权后的词条命中数进行过滤。",
    ],
    [
      `Only relics that have more than the specified number of weighted rolls will be used for the optimization search.`,
      "只有计算权重之后词条数量超过指定阈值的遗器才会被优化器检索。",
    ],
    [
      `Note that setting the minimum rolls too low may result in some builds not being displayed, if the filter ends up excludes a key relic. Use this filter with caution, but on large searches it makes a large impact on reducing search time.`,
      "需要注意的是，将遗器的最低加权词条数量设置得太低可能会导致过滤器排除某个关键遗器，导致某些构筑无法显示。请谨慎使用该过滤器，即使它在大型检索中对缩短检索时间有显著影响。",
    ],
    [
      `Min (left) / Max (right) filters for character stats, inclusive. The optimizer will only show results within these ranges`,
      "角色属性将被限定在筛选器规定的阈值内，左侧为最小值，右侧为最大值，包含临界值在内。优化器将只会显示这些范围内的结果。",
    ],
    [
      `Stat abbreviations are ATK / HP / DEF / SPD / Crit Rate / Crit Damage / Effect Hit Rate / Effect RES / Break Effect`,
      "部分属性名因UI空间问题采用了缩写。",
    ],
    [
      `NOTE: Ingame speed decimals are truncated so you may see speed values ingame higher than shown here. This is because the OCR importer can't detect the hidden decimals.`,
      "注意：游戏中面板显示的速度是取整的，因此您在游戏中看到的速度值可能高于此处显示的值。如果您使用基于 OCR 的方式导入遗器，计算器将无法检测到被隐藏的速度值小数点。",
    ],
    [
      `Weight - Sum of substat weights of all 6 relics, from the Substat weight filter`,
      '权重 - 所有部位遗器的权重值之和，根据"副属性权重过滤"区域的设置计算',
    ],
    [
      `Ehp - Effective HP, measuring how tanky a max level character is. Calculated using HP & DEF & damage reduction passives`,
      "有效生命 - 评估一个最高等级的角色有多耐揍。根据生命值、防御力和减伤被动来计算。",
    ],
    [
      `Basic / Skill / Ult / Fua (Follow-up attack) / Dot (Damage over time) - Skill damage calculations, based on the environmental factors in character passives / light cone passives / enemy options.`,
      "普攻/战技/终结技/追加攻击/持续伤害 - 计算技能的伤害，基于角色被动/光锥被动/敌人等选项的环境因素。",
    ],
    /*[
              ``,
              ''
          ],*/
  ]);

  const alertbak = window.alert.bind(window);
  window.alert = (message) => {
    if (i18n.has(message)) message = i18n.get(message);
    return alertbak(message);
  };

  const confirmbak = window.confirm.bind(window);
  window.confirm = (message) => {
    if (i18n.has(message)) message = i18n.get(message);
    return confirmbak(message);
  };

  const promptbak = window.prompt.bind(window);
  window.prompt = (message, _default) => {
    if (i18n.has(message)) message = i18n.get(message);
    return promptbak(message, _default);
  };

  replaceText(document.body);

  const bodyObserver = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((addedNode) => replaceText(addedNode));
    });
  });
  bodyObserver.observe(document.body, { childList: true, subtree: true });

  function cleanStr(str) {
    if (!str) return str;
    return str.replace(/^\s+|\s+$/gm, "");
  }

  function getReplace(ori, key, value) {
    return ori?.replace(key, cleanStr(value));
  }

  function replaceText(node) {
    nodeForEach(node).forEach((textNode) => {
      const nodeValue = cleanStr(textNode.nodeValue);
      const innerText = cleanStr(textNode.innerText);
      const tNodeValue = cleanStr(textNode.value);
      const placeHolder = cleanStr(textNode.placeholder);

      function replaceIfMatch(text) {
        for (let [key, value] of i18n) {
          const regex = new RegExp(`^\\(\\d+\\) ${key}$`);
          if (regex.test(text)) {
            return text.replace(key, value);
          } else if (Array.isArray(key)) {
            for (let k of key) {
              if (k instanceof RegExp && k.test(text)) {
                return text.replace(k, value);
              } else if (text === k) {
                return value;
              }
            }
          } else {
            if (key instanceof RegExp && key.test(text)) {
              return text.replace(key, value);
            } else if (text === key) {
              return value;
            }
          }
        }
        return text;
      }

      if (textNode instanceof Text) {
        textNode.nodeValue = replaceIfMatch(nodeValue);
      } else if (textNode.innerText) {
        textNode.innerText = replaceIfMatch(innerText);
      } else if (textNode instanceof HTMLInputElement) {
        if (textNode.type === "button") {
          textNode.value = replaceIfMatch(tNodeValue);
        } else if ("text;password;search".indexOf(textNode.type) >= 0) {
          textNode.placeholder = replaceIfMatch(placeHolder);
        }
      }
    });
  }

  function nodeForEach(node) {
    const list = [];
    if (node.childNodes.length === 0) list.push(node);
    else {
      node.childNodes.forEach((child) => {
        if (child.childNodes.length === 0) list.push(child);
        else list.push(...nodeForEach(child));
      });
    }
    return list;
  }

  function observeDropdown(dropdown) {
    const dropdownObserver = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (
          mutation.type === "attributes" &&
          mutation.attributeName === "title"
        ) {
          replaceText(mutation.target);
        }
      });
    });
    dropdownObserver.observe(dropdown, { attributes: true, subtree: true });
  }

  document
    .querySelectorAll(".ant-select-selection-item")
    .forEach(observeDropdown);

  const dropdownObserver = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((addedNode) => {
        if (addedNode.nodeType === Node.ELEMENT_NODE) {
          addedNode
            .querySelectorAll(".ant-select-selection-item")
            .forEach(observeDropdown);
        }
      });
    });
  });
  dropdownObserver.observe(document.body, { childList: true, subtree: true });
})();
