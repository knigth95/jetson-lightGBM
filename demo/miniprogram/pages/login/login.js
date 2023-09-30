const db = wx.cloud.database()
Page({


    signup: function () {
        wx.navigateTo({
            url: '/pages/signup/signup', //跳转到注册页面
        })
    },
    /**
     * 页面的初始数据
     */
    data: {
        user: {
            name: '',
            password: ''
        },
        cardCur: 0,
        swiperList: [{
            id: 0,
            type: 'image',
            url: '/image/scenery1.jpg'
        }, {
            id: 1,
            type: 'image',
            url: '/image/scenery2.jpg',
        }, {
            id: 2,
            type: 'image',
            url: '/image/scenery3.jpg'
        }, {
            id: 3,
            type: 'image',
            url: '/image/scenery4.jpg'
        }, {
            id: 4,
            type: 'image',
            url: '/image/scenery5.jpg'
        }, {
            id: 5,
            type: 'image',
            url: '/image/scenery6.jpg'
        }, {
            id: 6,
            type: 'image',
            url: '/image/scenery7.jpg'
        }],
    },

    inputName: function (event) {
        console.log(event.detail.value)
        this.data.user.name = event.detail.value
    },
    inputPassword: function (event) {
        console.log(event.detail.value)
        this.data.user.password = event.detail.value
    },
    loginEvent: function () {
        console.log(this.data.user)
        var user = this.data.user
        db.collection('user')
            .where({
                name: this.data.user.name,
                password: this.data.user.password

            })
            .get().then(res => {
                //res.date 包含该记录的数据
                console.log(res.data)
                if (res.data.length == 1) {
                    console.log("登录成功！")
                    try {
                      wx.setStorageSync('name', this.data.user.name);
                      console.log('代码执行成功');
                    } catch (error) {
                      console.error('代码执行失败:', error);
                    }
                    wx.showToast({
                        title: '成功',
                        icon: 'success',
                        duration: "2000"
                    })
                    console.log()
                    wx.navigateTo({
                        url: '../home/home',
                    })
                } else {
                    console.log("登录失败！")
                    wx.showToast({
                        title: '用户名或密码错误',
                        icon: 'none',
                        duration: "2000"
                    })
                }
            })

    },
    forget:function(){
        wx.navigateTo({
          url: '/pages/forget/forget',
        })
    },
    onLoad() {
        this.towerSwiper('swiperList');
        // 初始化towerSwiper 传已有的数组名即可
    },
    DotStyle(e) {
        this.setData({
            DotStyle: e.detail.value
        })
    },
    // cardSwiper
    cardSwiper(e) {
        this.setData({
            cardCur: e.detail.current
        })
    },
    // towerSwiper
    // 初始化towerSwiper
    towerSwiper(name) {
        let list = this.data[name];
        for (let i = 0; i < list.length; i++) {
            list[i].zIndex = parseInt(list.length / 2) + 1 - Math.abs(i - parseInt(list.length / 2))
            list[i].mLeft = i - parseInt(list.length / 2)
        }
        this.setData({
            swiperList: list
        })
    },
    // towerSwiper触摸开始
    towerStart(e) {
        this.setData({
            towerStart: e.touches[0].pageX
        })
    },
    // towerSwiper计算方向
    towerMove(e) {
        this.setData({
            direction: e.touches[0].pageX - this.data.towerStart > 0 ? 'right' : 'left'
        })
    },
    // towerSwiper计算滚动
    towerEnd(e) {
        let direction = this.data.direction;
        let list = this.data.swiperList;
        if (direction == 'right') {
            let mLeft = list[0].mLeft;
            let zIndex = list[0].zIndex;
            for (let i = 1; i < list.length; i++) {
                list[i - 1].mLeft = list[i].mLeft
                list[i - 1].zIndex = list[i].zIndex
            }
            list[list.length - 1].mLeft = mLeft;
            list[list.length - 1].zIndex = zIndex;
            this.setData({
                swiperList: list
            })
        } else {
            let mLeft = list[list.length - 1].mLeft;
            let zIndex = list[list.length - 1].zIndex;
            for (let i = list.length - 1; i > 0; i--) {
                list[i].mLeft = list[i - 1].mLeft
                list[i].zIndex = list[i - 1].zIndex
            }
            list[0].mLeft = mLeft;
            list[0].zIndex = zIndex;
            this.setData({
                swiperList: list
            })
        }
    }
})