/**
 * Created by 蟋蟀的林 on 2018/11/26.
 */
;
var upload = {
    error: function (msg) {
        common_ops.alert(msg);
    },
    success: function (file_key) {
        if (!file_key) {
            return;
        }
        var html = '<img src="' + common_ops.buildPicUrl(file_key) + '"/>'
                + '<span class="fa fa-times-circle del del_image" data="' + file_key + '"></span>';

        if ($(".upload_pic_wrap .pic-each").size() > 0) {      //判断这里是不是已经有了图片
            $(".upload_pic_wrap .pic-each").html(html);
        } else {
            $(".upload_pic_wrap").append('<span class="pic-each">' + html + '</span>');//拼一个pic-each 显示图片
        }
        book_newset_ops.delete_img();
    }
};
var book_newset_ops = {
    init: function () {
        this.ue = null;
        this.eventBind();
        this.initEditor();
        this.delete_img();
    },
    eventBind: function () {
        var that = this;

        $(".wrap_food_set .upload_pic_wrap input[name=pic]").change(function () {
            $(".wrap_food_set .upload_pic_wrap").submit();
        });
/*没有引入选择和tags的js，先注释掉这里
        $(".wrap_food_set select[name=cat_id]").select2({
            language: "zh-CN",
            width: '100%'
        });

        $(".wrap_food_set input[name=tags]").tagsInput({
            width: 'auto',
            height: 40,
            onAddTag: function (tag) {
            },
            onRemoveTag: function (tag) {
            }
        });
*/
        $(".wrap_food_set .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }
            var title_target = $(".wrap_food_set input[name=title]");
            var title = title_target.val();

            var author_target = $(".wrap_food_set input[name=author]");
            var author = author_target.val();

            var press_target = $(".wrap_food_set input[name=press]");
            var press = press_target.val();

            var cat_id_target = $(".wrap_food_set select[name=cat_id]");
            var cat_id = cat_id_target.val();   //这里获取的是选项的value值

            var intro_target = $(".wrap_food_set textarea[name=intro]");
            var intro = intro_target.val();

            var location_target = $('#location  option:selected');
            var location= location_target.text();

            var amount_target = $(".wrap_food_set input[name=amount]");
            var amount = amount_target.val();

            if (title.length < 1) {
                common_ops.tip("请输入符合规范的书名~~",title_target);
                return;
            }

            if (author.length < 1) {
                common_ops.tip("请输入符合规范的作者名~~",author_target);
                return;
            }

            if (press.length < 1) {
                common_ops.tip("请输入符合规范的出版社名称~~",press_target);
                return;
            }

            if ($(".wrap_food_set .pic-each").size() < 1) {
                common_ops.alert("请上传封面图~~");
                return;
            }

            if (cat_id.length < 1) {
                common_ops.tip("请选择分类~~", cat_id_target);
                return;
            }

            if (intro.length < 10) {
                common_ops.tip("请输入书籍简介，并不能少于10个字符~~", intro_target);
                return;
            }


            if (location.length < 1) {
                common_ops.tip("请输入符合规范的新书所在馆地点~~", location_target);
                return;
            }
            if (parseInt(amount) <= 0) {
                common_ops.tip("请输入符合规范的上新数量~~", intro_target);
                return;
            }


            btn_target.addClass("disabled");

            var data = {
                title:title,
                author:author,
                press:press,
                image: $(".wrap_food_set .pic-each .del_image").attr("data"),
                cat_id: cat_id,
                intro:intro,
                location:location,
                amount:amount,
                id: $(".wrap_food_set input[name=id]").val()
            };

            $.ajax({
                url: common_ops.buildUrl("/books_lib/new_set"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/books_lib/index");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });

        });


    },
    initEditor: function () {
        var that = this;

        that.ue = UE.getEditor('editor', {
            toolbars: [
                ['undo', 'redo', '|',
                    'bold', 'italic', 'underline', 'strikethrough', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', '|', 'rowspacingtop', 'rowspacingbottom', 'lineheight'],
                ['customstyle', 'paragraph', 'fontfamily', 'fontsize', '|',
                    'directionalityltr', 'directionalityrtl', 'indent', '|',
                    'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|', 'touppercase', 'tolowercase', '|',
                    'link', 'unlink'],
                ['imagenone', 'imageleft', 'imageright', 'imagecenter', '|',
                    'insertimage', 'insertvideo', '|',
                    'horizontal', 'spechars', '|', 'inserttable', 'deletetable', 'insertparagraphbeforetable', 'insertrow', 'deleterow', 'insertcol', 'deletecol', 'mergecells', 'mergeright', 'mergedown', 'splittocells', 'splittorows', 'splittocols']

            ],
            enableAutoSave: true,
            saveInterval: 60000,
            elementPathEnabled: false,
            zIndex: 4,
            serverUrl: common_ops.buildUrl('/upload/ueditor')
        });
    },
    delete_img: function () {
        $(".wrap_food_set .del_image").unbind().click(function () {
            $(this).parent().remove();
        });
    }
};

$(document).ready(function () {
    book_newset_ops.init();
});