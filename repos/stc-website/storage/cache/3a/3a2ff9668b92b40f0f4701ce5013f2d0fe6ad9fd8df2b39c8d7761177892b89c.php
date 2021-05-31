<?php

/* default/template/common/home.twig */
class __TwigTemplate_0fb97f8a64ab2879f5ef0a75c130f7a8537129a4bbfb280c11f7cf78078708bc extends Twig_Template
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
        echo "
<div id=\"common-home\" class=\"container\">
  <div class=\"row\">";
        // line 3
        echo (isset($context["column_left"]) ? $context["column_left"] : null);
        // line 4
        if (((isset($context["column_left"]) ? $context["column_left"] : null) && (isset($context["column_right"]) ? $context["column_right"] : null))) {
            // line 5
            $context["class"] = "col-sm-6";
        } elseif ((        // line 6
(isset($context["column_left"]) ? $context["column_left"] : null) || (isset($context["column_right"]) ? $context["column_right"] : null))) {
            // line 7
            $context["class"] = "col-sm-9";
        } else {
            // line 9
            $context["class"] = "col-sm-12";
        }
        // line 11
        echo "    <div id=\"content\" class=\"";
        echo (isset($context["class"]) ? $context["class"] : null);
        echo "\">";
        echo (isset($context["content_top"]) ? $context["content_top"] : null);
        echo (isset($context["content_bottom"]) ? $context["content_bottom"] : null);
        echo "</div>";
        // line 12
        echo (isset($context["column_right"]) ? $context["column_right"] : null);
        echo "</div>
</div>";
        // line 14
        echo (isset($context["footer"]) ? $context["footer"] : null);
    }

    public function getTemplateName()
    {
        return "default/template/common/home.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  49 => 14,  45 => 12,  38 => 11,  35 => 9,  32 => 7,  30 => 6,  28 => 5,  26 => 4,  24 => 3,  19 => 1,);
    }
}
/* {{ header }}*/
/* <div id="common-home" class="container">*/
/*   <div class="row">{{ column_left }}*/
/*     {% if column_left and column_right %}*/
/*     {% set class = 'col-sm-6' %}*/
/*     {% elseif column_left or column_right %}*/
/*     {% set class = 'col-sm-9' %}*/
/*     {% else %}*/
/*     {% set class = 'col-sm-12' %}*/
/*     {% endif %}*/
/*     <div id="content" class="{{ class }}">{{ content_top }}{{ content_bottom }}</div>*/
/*     {{ column_right }}</div>*/
/* </div>*/
/* {{ footer }}*/
