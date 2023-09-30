
const db=wx.cloud.database()
Page({
    data: {
      name: '',
      password: '',
      confirm:''
    },
    //获取用户名
    getname(event) {
        console.log('获取输入的用户名', event.detail.value)
        this.setData({
            name: event.detail.value
        })
    },
    // 获取密码
    getpassword(event) {
      console.log('获取输入的密码', event.detail.value)
      this.setData({
        password: event.detail.value
      })
    },
    //确认密码
    confirm(event){
        console.log('确认的密码',event.detail.value)
        this.setData({
            confirm:event.detail.value
        })
    },
    //注册
    submit() {
      let name = this.data.name
      let password = this.data.password
      let confirm = this.data.confirm
      console.log("点击了注册")
      console.log("name", name)
      console.log("password", this.data.password)
      //校验用户名
    if (name.length < 2) {
        wx.showToast({
          icon: 'none',
          title: '用户名至少2位',
        })
        return
      }
      if (name.length > 10) {
        wx.showToast({
          icon: 'none',
          title: '用户名最多10位',
        })
        return
      }
      //校验密码
      if (password!=confirm) {
        wx.showToast({
          icon: 'none',
          title: '密码不一致',
        })
        return
      }
      //注册功能的实现
      db.collection('user').where({
          name:this.data.name
      })
      .get().then(res =>{
          console.log(res.data)
          if(res.data.length==0){
            db.collection('user').add({
                data: {
                  name: name,
                  password: password
                },
                success(res) {
                  console.log('注册成功', res)
                  wx.showToast({
                    icon: '',
                    title: '注册成功',
                  })
                  wx.showToast({
                    title: '注册成功',
                  })
                },
                fail(res) {
                  console.log('注册失败', res)
                  wx.showToast({
                    title: '注册失败',
                    icon: 'error',
                  })
                }
              })
          }
          else{
              wx.showToast({
                  icon:'error',
                title: '账户已存在',
                duration:2000
              })
          }
      })
    }
  })