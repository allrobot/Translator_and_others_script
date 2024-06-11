"auto";
auto.waitFor();
auto.setMode("fast");

/**
 * 返回数值
 * @param UiSelector widget：UiSelector对象
 * @returns number：数值，或返回null
 */
function getNumber(widget) {
  if (widget == null) {
    return null;
  }
  // 存储初始文本内容
  let initText = widget.text();
  // log(initText)
  let match = initText.match(/\d+/g);
  return match ? parseInt(match[0]) : null;
}

/**
 *  点击控件
 *  如果当前控件不可点击，则尝试点击父控件，最多限于3层父级
 *  @param widget：UiSelector对象，表示需要点击的控件
 *  @return boolean：是否成功点击
 */
function clickParentIfClickable(widget) {
  if (widget == null) {
    console.log("目标控件不存在");
  } else {
    // 循环三次
    let maxnum = 3;
    for (let i = 0; i < maxnum; i++) {
      if (widget.clickable() == false) {
        widget = widget.parent();
      } else {
        break;
      }
    }
    widget.click();
  }
}

/**
 * 检查当前页面是否为起点读书主界面
 */
function checkIsReadBook() {
  if (currentPackage() != "com.qidian.QDReader") {
    console.log("当前页面非目标应用，异常退出");
    exit();
  }
}

/**
 * 返回主界面
 */
function backHome() {
  while (id("normal").findOne(500) == null) {
    checkIsReadBook();
    let cancel_button = id("button_text_id")
      .className("android.widget.TextView")
      .text("取消")
      .findOne(500);
    if (cancel_button != null) {
      clickParentIfClickable(cancel_button);
    }
    closeTeenModeDialog();
    back();
  }
  let bookrack = id("view_tab_title_title").text("书架").findOnce();
  if (bookrack != null) {
    clickParentIfClickable(bookrack);
  }
}

/**
 * 关闭青少年模式弹窗
 */
function closeTeenModeDialog() {
  let teen_mode_dialog = id("button_text_id")
    .className("android.widget.TextView")
    .text("我知道了")
    .findOne(500);
  if (teen_mode_dialog != null) {
    console.log("关闭图片按钮");
    clickParentIfClickable(teen_mode_dialog);
  }
}

/**
 * 等待至某控件出现
 * @param widget：UiSelector对象，表示需要等待的控件
 * @param timeout：超时时间，单位毫秒，默认60秒
 * @param no_exit：是否不退出程序，默认false
 */
function waitForWidget(widget, timeout, no_exit) {
  if (timeout == null) {
    timeout = 60000;
  }
  if (no_exit == null) {
    no_exit = false;
  }
  if (widget == null) {
    console.log("目标控件不存在，无法等待出现");
    exit();
  }
  let now_time = new Date().getTime();
  while (widget.exists() == false) {
    checkIsReadBook();
    swipe(100, 150, 100, 200, 300);
    swipe(100, 200, 100, 150, 300);
    // 如果时间超过60秒，则退出
    if (new Date().getTime() - now_time > timeout) {
      console.log("等待" + widget + "超时");
      if (no_exit) {
        return false;
      } else {
        console.log("已退出");
        exit();
      }
    }
  }
  return true;
}

/**
 * 等待至某控件消失
 * @param widget：UiSelector对象，表示需要等待的控件
 * @param timeout：超时时间，单位毫秒，默认60秒
 * @param no_exit：是否不退出程序，默认false
 */
function waitForWidgetDisappear(widget, timeout, no_exit) {
  if (timeout == null) {
    timeout = 60000;
  }
  if (no_exit == null) {
    no_exit = false;
  }
  if (widget == null) {
    console.log("目标控件不存在，无法等待消失");
    exit();
  }
  let now_time = new Date().getTime();
  while (widget.exists() == true) {
    checkIsReadBook();
    swipe(100, 150, 100, 200, 300);
    swipe(100, 200, 100, 150, 300);
    // 如果时间超过60秒，则退出
    if (new Date().getTime() - now_time > timeout) {
      console.log("等待" + widget + "超时");
      if (no_exit) {
        return false;
      } else {
        console.log("已退出");
        exit();
      }
    }
  }
  return true;
}

var ok_button = className("android.view.View").depth(18).desc("我知道了");

/**
 * 确定“我知道了”弹窗
 */
function confirmDialog() {
  let ok_bool = waitForWidget(ok_button, 6000, true);
  if (ok_bool) {
    ok_button.findOnce().click();
  }
}

/**
 * 广告跳过
 */
function skipAd() {
  // 等待跳过广告出现

  waitclose = className("TextView").text("跳过广告");
  if (ok_button.findOnce(500) == null) {
    re_bool = waitForWidget(waitclose, 10000, true);
    // 等待广告关闭按钮出现
    if (re_bool) {
      waitForWidgetDisappear(waitclose);
      let closebutton = className("android.widget.ImageView").depth(5);
      waitForWidget(closebutton, 100000);
      if (closebutton.findOnce()) {
        closebutton.findOnce().click();
      }
    }
  }
}

/**
 * 打开视频看完后领取奖励
 * @param widget：UiSelector对象，表示视频控件
 */
function clickOkButton(widget) {
  findonce = widget.findOnce();
  if (findonce != null) {
    clickParentIfClickable(findonce);
    skipAd();
    confirmDialog();
  } else {
    throw new Error("观看广告发生了异常");
  }
}

/**
 * 进入起点读书主界面
 */
function enterReadBook() {
  console.log("执行 - 进入起点读书主界面");

  if (app.launch("com.qidian.QDReader")) {
    waitForPackage("com.qidian.QDReader");
  } else {
    console.log("起点应用不存在，请检查是否安装");
    exit();
  }
  if (id("splash_skip_button").findOnce(2000)) {
    console.log("跳过启动页");
    clickP;
    arentIfClickable(id("splash_skip_button").findOnce());
  }
  if (id("imgClose").findOnce(1000)) {
    console.log("关闭弹窗");
    clickParentIfClickable(id("imgClose").findOnce());
  }
  closeTeenModeDialog();
  backHome();
}

/**
 * 进入福利中心
 */
function enterFuliCenter() {
  console.log("执行 - 进入福利中心");

  // console.log("点击APK的个人界面“我”");
  // let wo = id("view_tab_title_title").text("我").findOnce();
  // clickParentIfClickable(wo);

  console.log("点击福利中心");
  let fulizhongxin = id("tvTitle").text("福利中心");
  waitForWidget(fulizhongxin);
  clickParentIfClickable(fulizhongxin.findOnce());

  console.log("正在等待网页加载完毕"); //output 0
  let watch3TimesAdLabel =
    className("android.view.View").text("额外看3次小视频得奖励");
  waitForWidget(watch3TimesAdLabel);
}

/**
 * 观看小视频广告
 */
function watchVideos() {
  // 观看8个小视频广告
  let watch_video_button1 = text("看视频领福利");
  if (watch_video_button1.exists()) {
    if (watch_video_button1.clickable()) {
      console.log("执行 - 观看8个小视频广告");
    }
    while (watch_video_button1.exists()) {
      checkIsReadBook();
      clickOkButton(watch_video_button1);
    }
  }
  // 点击看视频按钮
  let watch_video_button2 = text("看视频");
  if (watch_video_button2.exists()) {
    console.log("执行 - 观看三个小视频广告");
    while (watch_video_button2.exists()) {
      checkIsReadBook();
      clickOkButton(watch_video_button2);
    }
  }

  // 开宝箱
  let open_box = descStartsWith("看视频");
  if (open_box.exists()) {
    console.log("执行 - 看宝箱视频");
    clickOkButton(open_box);
    console.log("看完视频，已开宝箱了");
  }
}

/**
 * 听书一分钟
 */
function listenOneMinute() {
  let listen_book_label = className("android.view.View").text("当日听书1分钟");
  waitForWidget(listen_book_label);
  let listen_book = listen_book_label.findOnce().parent().child(3);
  if (listen_book.clickable() && listen_book.desc() == "去完成") {
    console.log("执行 - 听书1分钟");
    // 点击“去完成”按钮
    listen_book.click();
    waitForWidgetDisappear(listen_book_label);

    // 是否直接进入听书界面
    let listen_select = id("ivPlayOrPause").className(
      "android.widget.FrameLayout"
    );
    let listen_button = waitForWidget(listen_select, 10000, true);
    if (listen_button) {
      // 等待某书加载出现
      let one_book = id("playIv");
      console.log("正在等待小说加载完毕");
      console.log(one_book.exists());
      let one_book_bool = waitForWidget(one_book, 50000, true);
      if (one_book_bool) {
        clickParentIfClickable(one_book.findOnce());
        // 等到小说听书加载完毕
        let listen_one_minute_loading = id("tvTxtSrcLoading")
          .className("android.widget.TextView")
          .text("小说原文加载中...");
        console.log("正在听书中……");
        waitForWidget(listen_one_minute_loading);
        while (listen_one_minute_loading.exists()) {
          checkIsReadBook();
          sleep(1000);
        }
      }
    } else {
      console.log("正在听书中……");
    }
    sleep(63000);
    // 点击“暂停”按钮
    listen_select.findOnce().click();
    console.log("已听完1分钟");
    console.log("返回首页用于刷新页面");
    backHome();
    // 顺便关个听书悬浮弹窗
    let close_listen_button = id("ivClose").className(
      "android.widget.ImageView"
    );
    if (close_listen_button.exists()) {
      close_listen_button.findOnce().click();
    }
    enterFuliCenter();
  }
}

/**
 * 打游戏
 */
function playGame() {
  let play_game_label = className("android.view.View").text("当日玩游戏10分钟");
  waitForWidget(play_game_label);
  let play_game = play_game_label.findOnce().parent().child(3);
  if (play_game.clickable() && play_game.desc() == "去完成") {
    console.log("执行 - 玩游戏");
    // 点击“去完成”按钮
    play_game.click();
    // 等待游戏页面的一些控件加载完毕
    let progress_bar = id("browser_progress").className(
      "android.widget.ProgressBar"
    );
    waitForWidget(progress_bar);
    waitForWidgetDisappear(progress_bar, 120000);
    let classification_button = className("android.view.View").desc("分类");
    waitForWidget(classification_button);
    classification_button.findOnce().click();
    // 等待分类页面的一些控件加载完毕
    waitForWidget(progress_bar);
    waitForWidgetDisappear(progress_bar, 120000);
    let play_button = className("android.view.View").desc("在线玩");
    waitForWidget(play_button);
    play_button.findOnce().click();
    console.log("已点击按钮");
    waitForWidgetDisappear(play_button, 10000);
    // 检查是否进入游戏
    let game_title = className("android.webkit.WebView");
    waitForWidget(game_title);
    if (game_title != null) {
      let game_title = className("android.webkit.WebView");
      waitForWidget(game_title);
      if (game_title != null) {
        while (true) {
          checkIsReadBook();
          if (game_title.findOnce().text().length > 0) {
            console.log("已进入游戏");
            break;
          }
          sleep(1000);
        }
      }
      // 正在游玩中
      console.log("正在游玩中，请误操作");
      // 800秒，即14分，防止游戏加载过慢或卡顿
      sleep(800000);
      console.log("游戏结束，返回首页");
    } else {
      console.log("未进入游戏");
    }

    // 返回刷新界面
    backHome();
    enterFuliCenter();
  }
}

/**
 * 领取奖励
 */
function receiveAward() {
  while (true) {
    checkIsReadBook();
    let award_button = className("android.view.View").desc("领奖励").findOnce();
    if (award_button != null) {
      award_button.click();
      confirmDialog();
    } else {
      console.log("奖励已领取完毕");
      break;
    }
  }
  backHome();
}

/**
 * 签到领福利
 */
function signIn() {
  // 点击“签到福利”按钮
  let sign_in_button1 = text("签到福利");
  let sign_in_button2 = text("签到");
  if (sign_in_button1.exists() || sign_in_button2.exists()) {
    console.log("执行 - 签到领福利");
    function sign_in_button() {
      if (sign_in_button1.exists()) {
        clickParentIfClickable(sign_in_button1.findOnce());
      } else if (sign_in_button2.exists()) {
        clickParentIfClickable(sign_in_button2.findOnce());
        // 等待签到页面加载完毕
        let draw_lucky_button = className("android.widget.TextView").text(
          "免费抽奖"
        );
        let draw_lucky_button_bool = waitForWidget(
          draw_lucky_button,
          60000,
          true
        );
        if (draw_lucky_button_bool) {
          clickParentIfClickable(draw_lucky_button.findOnce());
        }
      }
      // 等待签到页面加载完毕
      console.log('等待"签到"页面加载完毕');
      let progress_bar = id("browser_progress").className(
        "android.widget.ProgressBar"
      );
      return waitForWidgetDisappear(progress_bar, 10000, true);
    }

    if (sign_in_button() == false) {
      console.log("签到加载超时，退出");
    } else {
      waitForWidget(className("android.view.View").text("· 为你推荐 ·"));

      // 免费抽奖
      let draw_lucky_button = className("android.view.View").text("点击抽奖+1");
      waitForWidget(draw_lucky_button);
      if (draw_lucky_button != null) {
        draw_lucky_button.findOnce().click();
        let residue_Lucky_number = className("android.view.View")
          .depth(16)
          .textContains("剩余");
        while (true) {
          waitForWidget(residue_Lucky_number);
          checkIsReadBook();
          let number = getNumber(residue_Lucky_number.findOnce());
          // console.log("剩余抽奖次数" + number);
          if (number > 0) {
            let button_Lucky_draw =
              className("android.view.View").desc("抽 奖");
            if (button_Lucky_draw.exists()) {
              console.log("开始抽奖");
              button_Lucky_draw.findOnce().click();
            }
          }
          let add_Lucky_button =
            className("android.view.View").desc("看视频抽奖喜+1");
          let add_Lucky_button_bool = waitForWidget(
            add_Lucky_button,
            5000,
            true
          );

          if (add_Lucky_button_bool) {
            console.log("观看广告抽奖次+1");
            add_Lucky_button.findOnce().click();
            skipAd();
          } else {
            break;
          }
        }
        console.log("没有抽奖次数了");
      }
      if (new Date().getDay() == 7) {
        let exchange_button =
          className("android.view.View").text("周日兑换章节卡");
        let exchange_button_bool = waitForWidget(exchange_button, 5000, true);
        if (exchange_button_bool) {
          if (exchange_button.findOnce().parent().clickable()) {
            console.log("周日兑换章节卡");
            exchange_button.findOnce().parent().click();
            waitForWidget(className("android.view.View").text("兑换章节卡"));
            let convertibility = getNumber(
              className("android.view.View")
                .textContains("张碎片可兑换")
                .findOnce()
            );
            if (convertibility > 0) {
              if (convertibility == 30) {
                let exchange_button_number = className(
                  "android.widget.TextView"
                ).text("30张碎片兑换");
              } else if (convertibility >= 20) {
                let exchange_button_number = className(
                  "android.widget.TextView"
                ).text("20张碎片兑换");
              } else if (convertibility >= 15) {
                let exchange_button_number = className(
                  "android.widget.TextView"
                ).text("15张碎片兑换");
              }
              let exchange_button_number = exchange_button_number
                .findOnce()
                .parent()
                .child(2);
              exchange_button_number.click();
              let click_button = className("android.view.View").desc("取消");
              let click_button_bool = waitForWidget(click_button, 5000, true);
              if (click_button_bool) {
                click_button.findOnce().parent().child(3).click();
              }
            }
          }
        }
      }
    }
    backHome();
    return;
  }
}

/**
 * 福利中心主流程
 */
function fuliCenterMain() {
  enterFuliCenter();
  watchVideos();
  listenOneMinute();
  playGame();
  receiveAward();
}

enterReadBook();

fuliCenterMain();

signIn();
