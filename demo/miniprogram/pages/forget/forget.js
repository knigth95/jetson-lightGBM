const db = wx.cloud.database();
Page({

  data: {
    user: {
      name: '',
      password: '',
      number:''
    }
  },

  name(event) {
      console.log('获取输入的用户名', event.detail.value)
      this.setData({
          name: event.detail.value
      })
  },

  number(event) {
    console.log('获取输入的手机号', event.detail.value)
    this.setData({
      number: event.detail.value
    })
  },

  getpassword(event) {
    console.log('获取输入的新密码', event.detail.value)
    this.setData({
      newpassword: event.detail.value
    })
  },


  change() {
    var name = this.data.name
    let number = this.data.number
    let newpassword = this.data.newpassword
    let userCollection = db.collection('user')
    console.log("test"+this.data.name)
    userCollection.where({
        name:this.data.name
    })
    .get().then(res =>{
        console.log(res.data)
        if(res.data.length==0){
            wx.showToast({
                icon: 'none',
                title: '用户名不存在',
              })
              return
        }
        else if (res.data[0].number != number) {
          wx.showToast({
            icon: 'none',
            title: '手机号或用户名错误',
          })
          return
        } else if (newpassword.length < 2 || newpassword.length > 10) {
          wx.showToast({
            icon: 'none',
            title: '密码长度应大于2小于10',
          })
          return
        } else {
          userCollection.where({
              name: name
            })
            .update({
              data: {
                password: newpassword
              }
            })
            .then(res => {
              console.log('更新成功')
              wx.showToast({
                icon: '',
                title: '更新成功',
              })
              this.setData({
                password: newpassword,
              })
            }).catch(err => {
              console.log('更新失败', err) //失败提示错误信息
            })
        }
      })
  },


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})
