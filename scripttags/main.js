function loadSettings(data) {
  $("#HeaderLogo img").attr("src", data.logo.img_link);
  $.each(data.menu, function (idx, item) {
    $("#MainMenu ul").append(
      '<li title="' +
        item.title +
        '"><a href="' +
        item.external_link +
        '"><span>' +
        item.title +
        "</span></a></li>"
    );
  });
  $.each(data.banner, function (idx, item) {
    console.log(item);
    if (item.activate == 1) {
      console.log(item.external_link);
      $("#MainBanners").append(
        '<div><a href="' +
          item.external_link +
          '"><img src="' +
          item.img_link +
          '" style="width: auto; height: 193px;"></a></div>'
      );
    }
  });
}

$(function () {
  $.ajax({
    type: "GET",
    url: "${SERVER_NAME}/api/settings",
    success: function (data) {
      console.log(data);
      loadSettings(data);
    },
  });
});
