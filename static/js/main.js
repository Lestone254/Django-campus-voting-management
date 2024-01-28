        $(".memelike").dblclick(function (e) {
          e.preventDefault()
              var id = $(this).attr('memeid');
              var meme= $(this).attr('like');
          $.ajax({
              url: '{%url 'like'%}',
              data: {
                  'id': id
                },
              dataType: 'json',
              success: function (data) {
              $(meme).text(data.likes);
              }
              });
        });

                $(".meme").click(function (e) {
          e.preventDefault()
              var id = $(this).attr('id');
              var meme= $(this).attr('like');
          $.ajax({
              url: '{%url 'like'%}',
              data: {
                  'id': id
                },
              dataType: 'json',
              success: function (data) {
              $(meme).text(data.likes);
              }
              });
        });