// pages/sleeptime/sleeptime.js
const db = wx.cloud.database()
Page({
  data: {
    sleepDuration: 7.5,
    timeimg: '/image/logo.jpg',// 
    selectedDate: '请选择日期',
    showPicker: '0',
    sleepage:'',
    efficiency:'',
    deepsleeptime:'',
    sleeptime:'',
    effectivetime:'',
    deepwaterratio:'',
  },

  showDatePicker() {
    this.setData({
      showPicker: true
    });
  },
  onDateChange(event) {
    const selectedDate = event.detail.value;
    this.setData({
      selectedDate: selectedDate,
      showPicker: false
    });
    db.collection('user').where({
      name:this.data.name
    }).get().then(res => {
      let foundimg=false;
      console.log(res.data)

      const dataArray=res.data
      dataArray.forEach(item =>{
        const rate=item.data
        console.log(rate)
        console.log('.........')
        rate.forEach(rateItem =>{
          const date=rateItem.date
          console.log(date)
          console.log(this.data.selectedDate)
          if(date==this.data.selectedDate){
            this.setData({
              timeimg: rateItem.imgID
            })
            console.log(rateItem.imgID)
            foundimg=1;
            return;
          }
        })
        if(foundimg){
          return;
        }
      })
      if(foundimg){
        return;
      }
    })
  },
  /**
   * 页面的初始数据
   */
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    const name = wx.getStorageSync('name')
        this.setData({
            name: name
        });
    console.log('欢迎'+this.data.name)
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