function previewImage(inputId, imgId, checkId) {
  var file = $("#" + inputId)[0].files[0];
  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = function (e) {
    $("#" + imgId).attr("src", e.target.result);
    if (checkId) $("#" + checkId).attr("checked", true);
  };
}

$("#LogoImageUpload").on("change", function () {
  previewImage("LogoImageUpload", "LogoImage");
});
$("#BannerImageUpload1").on("change", function () {
  previewImage("BannerImageUpload1", "BannerImage1", "BannerImageCheck1");
});
$("#BannerImageUpload2").on("change", function () {
  previewImage("BannerImageUpload2", "BannerImage2", "BannerImageCheck2");
});
$("#BannerImageUpload3").on("change", function () {
  previewImage("BannerImageUpload3", "BannerImage3", "BannerImageCheck3");
});
$("#BannerImageUpload4").on("change", function () {
  previewImage("BannerImageUpload4", "BannerImage4", "BannerImageCheck4");
});

/*
for (var i=1; i<=4; i++) {
  console.log("#BannerImageUpload" + i);
  $("#BannerImageUpload" + i).on("change", function () {previewImage("BannerImageUpload", "BannerImage", ""+i)});
}
*/

function imageUpload(target) {
  var imageUrl;
  $.ajax({
    type: "POST",
    url: "${SERVER_NAME}/api/image",
    data: {
      image: $("#" + target).attr("src"),
    },
    async: false,
    success: function (data) {
      console.log(data);
      if (data.message == "OK") {
        imageUrl = data.data.images[0].path;
      } else {
        alert(data.data.error.message);
      }
    },
  });
  return imageUrl;
}

var prevData = {};
$(function () {
  $.ajax({
    type: "GET",
    url: "${SERVER_NAME}:8000/api/settings",
    success: function (data) {
      console.log(data);
      prevData = data;
      loadPrevData();
    },
  });
});

function loadPrevData() {
  $("#LogoImage").attr("src", prevData.logo.img_link);

  $.each(prevData.menu, function (idx, item) {
    $("#MainMenuTitle" + (idx + 1)).val(item.title);
    $("#MainMenuLink" + (idx + 1)).val(item.external_link);
  });

  $.each(prevData.banner, function (idx, item) {
    $("#BannerImage" + (idx + 1)).attr("src", item.img_link);
    $("#BannerImageLink" + (idx + 1)).val(item.external_link);
    $("#BannerImageCheck" + (idx + 1)).attr("checked", item.activate == 1);
  });
}

function save() {
  var data = {};

  $("#UpdateStatus").text("로고 업로드 중...");
  if ($("#LogoImageUpload")[0].files.length > 0) {
    data.logo = {};
    data.logo.img_link = imageUpload("LogoImage");
  }

  $.each(prevData.menu, function (idx, item) {
    var tmp = {
      num: idx + 1,
    };
    if (prevData.menu[idx].title != $("#MainMenuTitle" + (idx + 1)).val())
      tmp.title = $("#MainMenuTitle" + (idx + 1)).val();
    if (
      prevData.menu[idx].external_link != $("#MainMenuLink" + (idx + 1)).val()
    )
      tmp.external_link = $("#MainMenuLink" + (idx + 1)).val();

    if (Object.keys(tmp).length > 1) {
      if (!data.menu) data.menu = [];
      data.menu.push(tmp);
    }
  });

  $("#UpdateStatus").text("배너 업로드 중...");
  $.each(prevData.banner, function (idx, item) {
    var tmp = {
      num: idx + 1,
    };
    if ($("#BannerImageUpload" + (idx + 1))[0].files.length > 0)
      tmp.img_link = imageUpload("BannerImage" + (idx + 1));
    if (
      prevData.banner[idx].external_link !=
      $("#BannerImageLink" + (idx + 1)).val()
    )
      tmp.external_link = $("#BannerImageLink" + (idx + 1)).val();
    if (
      (prevData.banner[idx].activate == 1) !=
      $("#BannerImageCheck" + (idx + 1)).is(":checked")
    )
      tmp.activate = $("#BannerImageCheck" + (idx + 1)).is(":checked") ? 1 : 0;

    if (Object.keys(tmp).length > 1) {
      if (!data.banner) data.banner = [];
      data.banner.push(tmp);
    }
  });

  console.log(data);

  $("#UpdateStatus").text("서버에 데이터 업로드 중...");
  $.ajax({
    type: "PUT",
    url: "${SERVER_NAME}/api/settings",
    data: JSON.stringify(data),
    async: false,
    contentType: "application/json",
    dataType: "json",
    success: function (data) {
      console.log(data);
      if (data.message == "OK") {
        alert("적용 완료!");
        window.location.reload();
      } else {
        alert(data.data.error.message);
      }
    },
  });

  $("#UpdateStatus").text("");
}
