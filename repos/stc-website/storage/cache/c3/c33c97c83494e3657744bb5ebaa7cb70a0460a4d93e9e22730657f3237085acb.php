<?php

/* tool/backup.twig */
class __TwigTemplate_4293210da311fa5adf8f64dc8fdd59f676a363d5780643b254f483763f185dc6 extends Twig_Template
{
    public function __construct(Twig_Environment $env)
    {
        parent::__construct($env);

        $this->parent = false;

        $this->blocks = array(
        );
    }

    protected function doDisplay(array $context, array $blocks = array())
    {
        // line 1
        echo (isset($context["header"]) ? $context["header"] : null);
        echo (isset($context["column_left"]) ? $context["column_left"] : null);
        echo "
<div id=\"content\">
  <div class=\"page-header\">
    <div class=\"container-fluid\">
      <h1>";
        // line 5
        echo (isset($context["heading_title"]) ? $context["heading_title"] : null);
        echo "</h1>
      <ul class=\"breadcrumb\">";
        // line 7
        $context['_parent'] = $context;
        $context['_seq'] = twig_ensure_traversable((isset($context["breadcrumbs"]) ? $context["breadcrumbs"] : null));
        foreach ($context['_seq'] as $context["_key"] => $context["breadcrumb"]) {
            // line 8
            echo "        <li><a href=\"";
            echo $this->getAttribute($context["breadcrumb"], "href", array());
            echo "\">";
            echo $this->getAttribute($context["breadcrumb"], "text", array());
            echo "</a></li>";
        }
        $_parent = $context['_parent'];
        unset($context['_seq'], $context['_iterated'], $context['_key'], $context['breadcrumb'], $context['_parent'], $context['loop']);
        $context = array_intersect_key($context, $_parent) + $_parent;
        // line 10
        echo "      </ul>
    </div>
  </div>
  <div class=\"container-fluid\">";
        // line 13
        if ((isset($context["error_warning"]) ? $context["error_warning"] : null)) {
            // line 14
            echo "    <div class=\"alert alert-danger alert-dismissible\"><i class=\"fa fa-exclamation-circle\"></i>";
            echo (isset($context["error_warning"]) ? $context["error_warning"] : null);
            echo "
      <button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button>
    </div>";
        }
        // line 18
        if ((isset($context["success"]) ? $context["success"] : null)) {
            // line 19
            echo "    <div class=\"alert alert-success alert-dismissible\"><i class=\"fa fa-check-circle\"></i>";
            echo (isset($context["success"]) ? $context["success"] : null);
            echo "
      <button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button>
    </div>";
        }
        // line 23
        echo "    <div class=\"panel panel-default\">
      <div class=\"panel-heading\">
        <h3 class=\"panel-title\"><i class=\"fa fa-exchange\"></i>";
        // line 25
        echo (isset($context["heading_title"]) ? $context["heading_title"] : null);
        echo "</h3>
      </div>
      <div class=\"panel-body\">
        <ul class=\"nav nav-tabs\">
          <li class=\"active\"><a href=\"#tab-backup\" data-toggle=\"tab\">";
        // line 29
        echo (isset($context["tab_backup"]) ? $context["tab_backup"] : null);
        echo "</a></li>
          <li><a href=\"#tab-restore\" data-toggle=\"tab\">";
        // line 30
        echo (isset($context["tab_restore"]) ? $context["tab_restore"] : null);
        echo "</a></li>
        </ul>
        <div class=\"tab-content\">
          <div class=\"tab-pane active\" id=\"tab-backup\">
            <form action=\"";
        // line 34
        echo (isset($context["export"]) ? $context["export"] : null);
        echo "\" method=\"post\" enctype=\"multipart/form-data\" id=\"form-export\" class=\"form-horizontal\">
              <div class=\"form-group\">
                <label class=\"col-sm-2 control-label\">";
        // line 36
        echo (isset($context["entry_export"]) ? $context["entry_export"] : null);
        echo "</label>
                <div class=\"col-sm-10\">
                  <div class=\"well well-sm\" style=\"height: 150px; overflow: auto;\">";
        // line 38
        $context['_parent'] = $context;
        $context['_seq'] = twig_ensure_traversable((isset($context["tables"]) ? $context["tables"] : null));
        foreach ($context['_seq'] as $context["_key"] => $context["table"]) {
            // line 39
            echo "                    <div class=\"checkbox\">
                      <label>
                        <input type=\"checkbox\" name=\"backup[]\" value=\"";
            // line 41
            echo $context["table"];
            echo "\" checked=\"checked\" />";
            // line 42
            echo $context["table"];
            echo "</label>
                    </div>";
        }
        $_parent = $context['_parent'];
        unset($context['_seq'], $context['_iterated'], $context['_key'], $context['table'], $context['_parent'], $context['loop']);
        $context = array_intersect_key($context, $_parent) + $_parent;
        // line 44
        echo " </div>
                  <button type=\"button\" onclick=\"\$(this).parent().find(':checkbox').prop('checked', true);\" class=\"btn btn-link\">";
        // line 45
        echo (isset($context["text_select_all"]) ? $context["text_select_all"] : null);
        echo "</button>
                  /
                  <button type=\"button\" onclick=\"\$(this).parent().find(':checkbox').prop('checked', false);\" class=\"btn btn-link\">";
        // line 47
        echo (isset($context["text_unselect_all"]) ? $context["text_unselect_all"] : null);
        echo "</button>
                </div>
              </div>
              <div class=\"form-group\">
                <div class=\"col-sm-10 col-sm-offset-2\">
                  <button type=\"submit\" form=\"form-export\" class=\"btn btn-default\"><i class=\"fa fa-download\"></i>";
        // line 52
        echo (isset($context["button_export"]) ? $context["button_export"] : null);
        echo "</button>
                </div>
              </div>
            </form>
          </div>
          <div class=\"tab-pane\" id=\"tab-restore\">
            <form class=\"form-horizontal\">
              <div class=\"form-group\">
                <label class=\"col-sm-2 control-label\">";
        // line 60
        echo (isset($context["entry_progress"]) ? $context["entry_progress"] : null);
        echo "</label>
                <div class=\"col-sm-10\">
                  <div id=\"progress-import\" class=\"progress\">
                    <div class=\"progress-bar\" role=\"progressbar\" aria-valuenow=\"0\" aria-valuemin=\"0\" aria-valuemax=\"100\"></div>
                  </div>
                </div>
              </div>
              <div class=\"form-group\">
                <div class=\"col-sm-10 col-sm-offset-2\">
                  <button type=\"button\" id=\"button-import\" class=\"btn btn-primary\"><i class=\"fa fa-upload\"></i>";
        // line 69
        echo (isset($context["button_import"]) ? $context["button_import"] : null);
        echo "</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
  <script type=\"text/javascript\"><!--
\$('#button-import').on('click', function() {
\t\$('#form-upload').remove();
\t
\t\$('body').prepend('<form enctype=\"multipart/form-data\" id=\"form-upload\" style=\"display: none;\"><input type=\"file\" name=\"import\" /></form>');
\t
\t\$('#form-upload input[name=\\'import\\']').trigger('click');
\t
\tif (typeof timer != 'undefined') {
\t\tclearInterval(timer);
\t}
\t
\ttimer = setInterval(function() {
\t\tif (\$('#form-upload input[name=\\'import\\']').val() != '') {
\t\t\tclearInterval(timer);
\t
\t\t\t\$('#progress-import .progress-bar').attr('aria-valuenow', 0);
\t\t\t\$('#progress-import .progress-bar').css('width', '0%');
\t
\t\t\t\$.ajax({
\t\t\t\turl: 'index.php?route=tool/backup/import&user_token=";
        // line 98
        echo (isset($context["user_token"]) ? $context["user_token"] : null);
        echo "',
\t\t\t\ttype: 'post',
\t\t\t\tdataType: 'json',
\t\t\t\tdata: new FormData(\$('#form-upload')[0]),
\t\t\t\tcache: false,
\t\t\t\tcontentType: false,
\t\t\t\tprocessData: false,
\t\t\t\tbeforeSend: function() {
\t\t\t\t\t\$('#button-import').button('loading');
\t\t\t\t},
\t\t\t\tcomplete: function() {
\t\t\t\t\t\$('#button-import').button('reset');
\t\t\t\t},
\t\t\t\tsuccess: function(json) {
\t\t\t\t\t\$('.alert-dismissible').remove();
\t\t\t\t\t
\t\t\t\t\tif (json['error']) {
\t\t\t\t\t\t\$('#content > .container-fluid').prepend('<div class=\"alert alert-danger alert-dismissible\"><i class=\"fa fa-exclamation-circle\"></i> ' + json['error'] + ' <button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button></div>');
\t\t\t\t\t}
\t\t\t\t\t
\t\t\t\t\tif (json['success']) {
\t\t\t\t\t\t\$('#content > .container-fluid').prepend('<div class=\"alert alert-success alert-dismissible\"><i class=\"fa fa-check-circle\"></i> ' + json['success'] + ' <button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button></div>');
\t\t\t\t\t}
\t\t\t\t\t
\t\t\t\t\tif (json['total']) {
\t\t\t\t\t\t\$('#progress-import .progress-bar').attr('aria-valuenow', json['total']);
\t\t\t\t\t\t\$('#progress-import .progress-bar').css('width', json['total'] + '%');
\t\t\t\t\t}
\t\t\t\t\t
\t\t\t\t\tif (json['next']) {
\t\t\t\t\t\tnext(json['next']);
\t\t\t\t\t}
\t\t\t\t},
\t\t\t\terror: function(xhr, ajaxOptions, thrownError) {
\t\t\t\t\talert(thrownError + \"\\r\\n\" + xhr.statusText + \"\\r\\n\" + xhr.responseText);
\t\t\t\t}
\t\t\t});
\t\t}
\t}, 500);
});

function next(url) {
\t\$.ajax({
\t\turl: url,
\t\tdataType: 'json',
\t\tsuccess: function(json) {
\t\t\t\$('.alert-dismissible').remove();
\t\t\t
\t\t\tif (json['error']) {
\t\t\t\t\$('#content > .container-fluid').prepend('<div class=\"alert alert-danger alert-dismissible\"><i class=\"fa fa-exclamation-circle\"></i> ' + json['error'] + ' <button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button></div>');
\t\t\t}
\t\t\t
\t\t\tif (json['success']) {
\t\t\t\t\$('#content > .container-fluid').prepend('<div class=\"alert alert-success alert-dismissible\"><i class=\"fa fa-check-circle\"></i> ' + json['success'] + ' <button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button></div>');
\t\t\t}
\t\t\t
\t\t\tif (json['total']) {
\t\t\t\t\$('#progress-import .progress-bar').attr('aria-valuenow', json['total']);
\t\t\t\t\$('#progress-import .progress-bar').css('width', json['total'] + '%');
\t\t\t}
\t\t\t
\t\t\tif (json['next']) {
\t\t\t\tnext(json['next']);
\t\t\t}
\t\t},
\t\terror: function(xhr, ajaxOptions, thrownError) {
\t\t\talert(thrownError + \"\\r\\n\" + xhr.statusText + \"\\r\\n\" + xhr.responseText);
\t\t}
\t});
}
  //--></script> 
</div>";
        // line 170
        echo (isset($context["footer"]) ? $context["footer"] : null);
        echo " ";
    }

    public function getTemplateName()
    {
        return "tool/backup.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  264 => 170,  190 => 98,  158 => 69,  146 => 60,  135 => 52,  127 => 47,  122 => 45,  119 => 44,  111 => 42,  108 => 41,  104 => 39,  100 => 38,  95 => 36,  90 => 34,  83 => 30,  79 => 29,  72 => 25,  68 => 23,  61 => 19,  59 => 18,  52 => 14,  50 => 13,  45 => 10,  35 => 8,  31 => 7,  27 => 5,  19 => 1,);
    }
}
/* {{ header }}{{ column_left }}*/
/* <div id="content">*/
/*   <div class="page-header">*/
/*     <div class="container-fluid">*/
/*       <h1>{{ heading_title }}</h1>*/
/*       <ul class="breadcrumb">*/
/*         {% for breadcrumb in breadcrumbs %}*/
/*         <li><a href="{{ breadcrumb.href }}">{{ breadcrumb.text }}</a></li>*/
/*         {% endfor %}*/
/*       </ul>*/
/*     </div>*/
/*   </div>*/
/*   <div class="container-fluid"> {% if error_warning %}*/
/*     <div class="alert alert-danger alert-dismissible"><i class="fa fa-exclamation-circle"></i> {{ error_warning }}*/
/*       <button type="button" class="close" data-dismiss="alert">&times;</button>*/
/*     </div>*/
/*     {% endif %}*/
/*     {% if success %}*/
/*     <div class="alert alert-success alert-dismissible"><i class="fa fa-check-circle"></i> {{ success }}*/
/*       <button type="button" class="close" data-dismiss="alert">&times;</button>*/
/*     </div>*/
/*     {% endif %}*/
/*     <div class="panel panel-default">*/
/*       <div class="panel-heading">*/
/*         <h3 class="panel-title"><i class="fa fa-exchange"></i> {{ heading_title }}</h3>*/
/*       </div>*/
/*       <div class="panel-body">*/
/*         <ul class="nav nav-tabs">*/
/*           <li class="active"><a href="#tab-backup" data-toggle="tab">{{ tab_backup }}</a></li>*/
/*           <li><a href="#tab-restore" data-toggle="tab">{{ tab_restore }}</a></li>*/
/*         </ul>*/
/*         <div class="tab-content">*/
/*           <div class="tab-pane active" id="tab-backup">*/
/*             <form action="{{ export }}" method="post" enctype="multipart/form-data" id="form-export" class="form-horizontal">*/
/*               <div class="form-group">*/
/*                 <label class="col-sm-2 control-label">{{ entry_export }}</label>*/
/*                 <div class="col-sm-10">*/
/*                   <div class="well well-sm" style="height: 150px; overflow: auto;"> {% for table in tables %}*/
/*                     <div class="checkbox">*/
/*                       <label>*/
/*                         <input type="checkbox" name="backup[]" value="{{ table }}" checked="checked" />*/
/*                         {{ table }}</label>*/
/*                     </div>*/
/*                     {% endfor %} </div>*/
/*                   <button type="button" onclick="$(this).parent().find(':checkbox').prop('checked', true);" class="btn btn-link">{{ text_select_all }}</button>*/
/*                   /*/
/*                   <button type="button" onclick="$(this).parent().find(':checkbox').prop('checked', false);" class="btn btn-link">{{ text_unselect_all }}</button>*/
/*                 </div>*/
/*               </div>*/
/*               <div class="form-group">*/
/*                 <div class="col-sm-10 col-sm-offset-2">*/
/*                   <button type="submit" form="form-export" class="btn btn-default"><i class="fa fa-download"></i> {{ button_export }}</button>*/
/*                 </div>*/
/*               </div>*/
/*             </form>*/
/*           </div>*/
/*           <div class="tab-pane" id="tab-restore">*/
/*             <form class="form-horizontal">*/
/*               <div class="form-group">*/
/*                 <label class="col-sm-2 control-label">{{ entry_progress }}</label>*/
/*                 <div class="col-sm-10">*/
/*                   <div id="progress-import" class="progress">*/
/*                     <div class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>*/
/*                   </div>*/
/*                 </div>*/
/*               </div>*/
/*               <div class="form-group">*/
/*                 <div class="col-sm-10 col-sm-offset-2">*/
/*                   <button type="button" id="button-import" class="btn btn-primary"><i class="fa fa-upload"></i> {{ button_import }}</button>*/
/*                 </div>*/
/*               </div>*/
/*             </form>*/
/*           </div>*/
/*         </div>*/
/*       </div>*/
/*     </div>*/
/*   </div>*/
/*   <script type="text/javascript"><!--*/
/* $('#button-import').on('click', function() {*/
/* 	$('#form-upload').remove();*/
/* 	*/
/* 	$('body').prepend('<form enctype="multipart/form-data" id="form-upload" style="display: none;"><input type="file" name="import" /></form>');*/
/* 	*/
/* 	$('#form-upload input[name=\'import\']').trigger('click');*/
/* 	*/
/* 	if (typeof timer != 'undefined') {*/
/* 		clearInterval(timer);*/
/* 	}*/
/* 	*/
/* 	timer = setInterval(function() {*/
/* 		if ($('#form-upload input[name=\'import\']').val() != '') {*/
/* 			clearInterval(timer);*/
/* 	*/
/* 			$('#progress-import .progress-bar').attr('aria-valuenow', 0);*/
/* 			$('#progress-import .progress-bar').css('width', '0%');*/
/* 	*/
/* 			$.ajax({*/
/* 				url: 'index.php?route=tool/backup/import&user_token={{ user_token }}',*/
/* 				type: 'post',*/
/* 				dataType: 'json',*/
/* 				data: new FormData($('#form-upload')[0]),*/
/* 				cache: false,*/
/* 				contentType: false,*/
/* 				processData: false,*/
/* 				beforeSend: function() {*/
/* 					$('#button-import').button('loading');*/
/* 				},*/
/* 				complete: function() {*/
/* 					$('#button-import').button('reset');*/
/* 				},*/
/* 				success: function(json) {*/
/* 					$('.alert-dismissible').remove();*/
/* 					*/
/* 					if (json['error']) {*/
/* 						$('#content > .container-fluid').prepend('<div class="alert alert-danger alert-dismissible"><i class="fa fa-exclamation-circle"></i> ' + json['error'] + ' <button type="button" class="close" data-dismiss="alert">&times;</button></div>');*/
/* 					}*/
/* 					*/
/* 					if (json['success']) {*/
/* 						$('#content > .container-fluid').prepend('<div class="alert alert-success alert-dismissible"><i class="fa fa-check-circle"></i> ' + json['success'] + ' <button type="button" class="close" data-dismiss="alert">&times;</button></div>');*/
/* 					}*/
/* 					*/
/* 					if (json['total']) {*/
/* 						$('#progress-import .progress-bar').attr('aria-valuenow', json['total']);*/
/* 						$('#progress-import .progress-bar').css('width', json['total'] + '%');*/
/* 					}*/
/* 					*/
/* 					if (json['next']) {*/
/* 						next(json['next']);*/
/* 					}*/
/* 				},*/
/* 				error: function(xhr, ajaxOptions, thrownError) {*/
/* 					alert(thrownError + "\r\n" + xhr.statusText + "\r\n" + xhr.responseText);*/
/* 				}*/
/* 			});*/
/* 		}*/
/* 	}, 500);*/
/* });*/
/* */
/* function next(url) {*/
/* 	$.ajax({*/
/* 		url: url,*/
/* 		dataType: 'json',*/
/* 		success: function(json) {*/
/* 			$('.alert-dismissible').remove();*/
/* 			*/
/* 			if (json['error']) {*/
/* 				$('#content > .container-fluid').prepend('<div class="alert alert-danger alert-dismissible"><i class="fa fa-exclamation-circle"></i> ' + json['error'] + ' <button type="button" class="close" data-dismiss="alert">&times;</button></div>');*/
/* 			}*/
/* 			*/
/* 			if (json['success']) {*/
/* 				$('#content > .container-fluid').prepend('<div class="alert alert-success alert-dismissible"><i class="fa fa-check-circle"></i> ' + json['success'] + ' <button type="button" class="close" data-dismiss="alert">&times;</button></div>');*/
/* 			}*/
/* 			*/
/* 			if (json['total']) {*/
/* 				$('#progress-import .progress-bar').attr('aria-valuenow', json['total']);*/
/* 				$('#progress-import .progress-bar').css('width', json['total'] + '%');*/
/* 			}*/
/* 			*/
/* 			if (json['next']) {*/
/* 				next(json['next']);*/
/* 			}*/
/* 		},*/
/* 		error: function(xhr, ajaxOptions, thrownError) {*/
/* 			alert(thrownError + "\r\n" + xhr.statusText + "\r\n" + xhr.responseText);*/
/* 		}*/
/* 	});*/
/* }*/
/*   //--></script> */
/* </div>*/
/* {{ footer }} */
