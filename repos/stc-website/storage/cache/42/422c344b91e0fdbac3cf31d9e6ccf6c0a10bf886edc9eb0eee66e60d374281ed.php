<?php

/* common/column_left.twig */
class __TwigTemplate_4efdcf2ce7aaa75dc8a72582defeb16ed3f1e19ff31bc63257f987b748e16c71 extends Twig_Template
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
        echo "<nav id=\"column-left\">
  <div id=\"navigation\"><span class=\"fa fa-bars\"></span>";
        // line 2
        echo (isset($context["text_navigation"]) ? $context["text_navigation"] : null);
        echo "</div>
  <ul id=\"menu\">";
        // line 4
        $context["i"] = 0;
        // line 5
        $context['_parent'] = $context;
        $context['_seq'] = twig_ensure_traversable((isset($context["menus"]) ? $context["menus"] : null));
        foreach ($context['_seq'] as $context["_key"] => $context["menu"]) {
            // line 6
            echo "    <li id=\"";
            echo $this->getAttribute($context["menu"], "id", array());
            echo "\">";
            if ($this->getAttribute($context["menu"], "href", array())) {
                echo "<a href=\"";
                echo $this->getAttribute($context["menu"], "href", array());
                echo "\"><i class=\"fa";
                echo $this->getAttribute($context["menu"], "icon", array());
                echo " fw\"></i>";
                echo $this->getAttribute($context["menu"], "name", array());
                echo "</a>";
            } else {
                echo "<a href=\"#collapse";
                echo (isset($context["i"]) ? $context["i"] : null);
                echo "\" data-toggle=\"collapse\" class=\"parent collapsed\"><i class=\"fa";
                echo $this->getAttribute($context["menu"], "icon", array());
                echo " fw\"></i>";
                echo $this->getAttribute($context["menu"], "name", array());
                echo "</a>";
            }
            // line 7
            if ($this->getAttribute($context["menu"], "children", array())) {
                // line 8
                echo "      <ul id=\"collapse";
                echo (isset($context["i"]) ? $context["i"] : null);
                echo "\" class=\"collapse\">";
                // line 9
                $context['_parent'] = $context;
                $context['_seq'] = twig_ensure_traversable($this->getAttribute($context["menu"], "children", array()));
                foreach ($context['_seq'] as $context["_key"] => $context["children_1"]) {
                    // line 10
                    echo "        <li>";
                    if ($this->getAttribute($context["children_1"], "href", array())) {
                        echo "<a href=\"";
                        echo $this->getAttribute($context["children_1"], "href", array());
                        echo "\">";
                        echo $this->getAttribute($context["children_1"], "name", array());
                        echo "</a>";
                    } else {
                        echo "<a href=\"#collapse";
                        echo (isset($context["i"]) ? $context["i"] : null);
                        echo "\" data-toggle=\"collapse\" class=\"parent collapsed\">";
                        echo $this->getAttribute($context["children_1"], "name", array());
                        echo "</a>";
                    }
                    // line 11
                    if ($this->getAttribute($context["children_1"], "children", array())) {
                        // line 12
                        echo "          <ul id=\"collapse";
                        echo (isset($context["i"]) ? $context["i"] : null);
                        echo "\" class=\"collapse\">";
                        // line 13
                        $context['_parent'] = $context;
                        $context['_seq'] = twig_ensure_traversable($this->getAttribute($context["children_1"], "children", array()));
                        foreach ($context['_seq'] as $context["_key"] => $context["children_2"]) {
                            // line 14
                            echo "            <li>";
                            if ($this->getAttribute($context["children_2"], "href", array())) {
                                echo "<a href=\"";
                                echo $this->getAttribute($context["children_2"], "href", array());
                                echo "\">";
                                echo $this->getAttribute($context["children_2"], "name", array());
                                echo "</a>";
                            } else {
                                echo "<a href=\"#collapse";
                                echo (isset($context["i"]) ? $context["i"] : null);
                                echo "\" data-toggle=\"collapse\" class=\"parent collapsed\">";
                                echo $this->getAttribute($context["children_2"], "name", array());
                                echo "</a>";
                            }
                            // line 15
                            if ($this->getAttribute($context["children_2"], "children", array())) {
                                // line 16
                                echo "              <ul id=\"collapse";
                                echo (isset($context["i"]) ? $context["i"] : null);
                                echo "\" class=\"collapse\">";
                                // line 17
                                $context['_parent'] = $context;
                                $context['_seq'] = twig_ensure_traversable($this->getAttribute($context["children_2"], "children", array()));
                                foreach ($context['_seq'] as $context["_key"] => $context["children_3"]) {
                                    // line 18
                                    echo "                <li><a href=\"";
                                    echo $this->getAttribute($context["children_3"], "href", array());
                                    echo "\">";
                                    echo $this->getAttribute($context["children_3"], "name", array());
                                    echo "</a></li>";
                                }
                                $_parent = $context['_parent'];
                                unset($context['_seq'], $context['_iterated'], $context['_key'], $context['children_3'], $context['_parent'], $context['loop']);
                                $context = array_intersect_key($context, $_parent) + $_parent;
                                // line 20
                                echo "              </ul>";
                            }
                            // line 21
                            echo " </li>";
                            // line 22
                            $context["i"] = ((isset($context["i"]) ? $context["i"] : null) + 1);
                        }
                        $_parent = $context['_parent'];
                        unset($context['_seq'], $context['_iterated'], $context['_key'], $context['children_2'], $context['_parent'], $context['loop']);
                        $context = array_intersect_key($context, $_parent) + $_parent;
                        // line 25
                        echo "          </ul>";
                    }
                    // line 26
                    echo "</li>";
                    // line 27
                    $context["i"] = ((isset($context["i"]) ? $context["i"] : null) + 1);
                }
                $_parent = $context['_parent'];
                unset($context['_seq'], $context['_iterated'], $context['_key'], $context['children_1'], $context['_parent'], $context['loop']);
                $context = array_intersect_key($context, $_parent) + $_parent;
                // line 29
                echo "      </ul>";
            }
            // line 30
            echo "</li>";
            // line 31
            $context["i"] = ((isset($context["i"]) ? $context["i"] : null) + 1);
        }
        $_parent = $context['_parent'];
        unset($context['_seq'], $context['_iterated'], $context['_key'], $context['menu'], $context['_parent'], $context['loop']);
        $context = array_intersect_key($context, $_parent) + $_parent;
        // line 33
        echo "  </ul>
  <div id=\"stats\">
    <ul>
      <li>
        <div>";
        // line 37
        echo (isset($context["text_complete_status"]) ? $context["text_complete_status"] : null);
        echo " <span class=\"pull-right\">";
        echo (isset($context["complete_status"]) ? $context["complete_status"] : null);
        echo "%</span></div>
        <div class=\"progress\">
          <div class=\"progress-bar progress-bar-success\" role=\"progressbar\" aria-valuenow=\"";
        // line 39
        echo (isset($context["complete_status"]) ? $context["complete_status"] : null);
        echo "\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width:";
        echo (isset($context["complete_status"]) ? $context["complete_status"] : null);
        echo "%\"> <span class=\"sr-only\">";
        echo (isset($context["complete_status"]) ? $context["complete_status"] : null);
        echo "%</span></div>
        </div>
      </li>
      <li>
        <div>";
        // line 43
        echo (isset($context["text_processing_status"]) ? $context["text_processing_status"] : null);
        echo " <span class=\"pull-right\">";
        echo (isset($context["processing_status"]) ? $context["processing_status"] : null);
        echo "%</span></div>
        <div class=\"progress\">
          <div class=\"progress-bar progress-bar-warning\" role=\"progressbar\" aria-valuenow=\"";
        // line 45
        echo (isset($context["processing_status"]) ? $context["processing_status"] : null);
        echo "\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width:";
        echo (isset($context["processing_status"]) ? $context["processing_status"] : null);
        echo "%\"> <span class=\"sr-only\">";
        echo (isset($context["processing_status"]) ? $context["processing_status"] : null);
        echo "%</span></div>
        </div>
      </li>
      <li>
        <div>";
        // line 49
        echo (isset($context["text_other_status"]) ? $context["text_other_status"] : null);
        echo " <span class=\"pull-right\">";
        echo (isset($context["other_status"]) ? $context["other_status"] : null);
        echo "%</span></div>
        <div class=\"progress\">
          <div class=\"progress-bar progress-bar-danger\" role=\"progressbar\" aria-valuenow=\"";
        // line 51
        echo (isset($context["other_status"]) ? $context["other_status"] : null);
        echo "\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width:";
        echo (isset($context["other_status"]) ? $context["other_status"] : null);
        echo "%\"> <span class=\"sr-only\">";
        echo (isset($context["other_status"]) ? $context["other_status"] : null);
        echo "%</span></div>
        </div>
      </li>
    </ul>
  </div>
</nav>
";
    }

    public function getTemplateName()
    {
        return "common/column_left.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  205 => 51,  198 => 49,  187 => 45,  180 => 43,  169 => 39,  162 => 37,  156 => 33,  150 => 31,  148 => 30,  145 => 29,  139 => 27,  137 => 26,  134 => 25,  128 => 22,  126 => 21,  123 => 20,  113 => 18,  109 => 17,  105 => 16,  103 => 15,  88 => 14,  84 => 13,  80 => 12,  78 => 11,  63 => 10,  59 => 9,  55 => 8,  53 => 7,  32 => 6,  28 => 5,  26 => 4,  22 => 2,  19 => 1,);
    }
}
/* <nav id="column-left">*/
/*   <div id="navigation"><span class="fa fa-bars"></span> {{ text_navigation }}</div>*/
/*   <ul id="menu">*/
/*     {% set i = 0 %}*/
/*     {% for menu in menus %}*/
/*     <li id="{{ menu.id }}">{% if menu.href %}<a href="{{ menu.href }}"><i class="fa {{ menu.icon }} fw"></i> {{ menu.name }}</a>{% else %}<a href="#collapse{{ i }}" data-toggle="collapse" class="parent collapsed"><i class="fa {{ menu.icon }} fw"></i> {{ menu.name }}</a>{% endif %}*/
/*       {% if menu.children %}*/
/*       <ul id="collapse{{ i }}" class="collapse">*/
/*         {% for children_1 in menu.children %}*/
/*         <li>{% if children_1.href %}<a href="{{ children_1.href }}">{{ children_1.name }}</a>{% else %}<a href="#collapse{{ i }}" data-toggle="collapse" class="parent collapsed">{{ children_1.name }}</a>{% endif %}*/
/*           {% if children_1.children %}*/
/*           <ul id="collapse{{ i }}" class="collapse">*/
/*             {% for children_2 in children_1.children %}*/
/*             <li>{% if children_2.href %}<a href="{{ children_2.href }}">{{ children_2.name }}</a>{% else %}<a href="#collapse{{ i }}" data-toggle="collapse" class="parent collapsed">{{ children_2.name }}</a>{% endif %}*/
/*               {% if children_2.children %}*/
/*               <ul id="collapse{{ i }}" class="collapse">*/
/*                 {% for children_3 in children_2.children %}*/
/*                 <li><a href="{{ children_3.href }}">{{ children_3.name }}</a></li>*/
/*                 {% endfor %}*/
/*               </ul>*/
/*               {% endif %} </li>*/
/*             {% set i = i + 1 %}*/
/*             */
/*             {% endfor %}*/
/*           </ul>*/
/*           {% endif %}</li>*/
/*         {% set i = i + 1 %}*/
/*         {% endfor %}*/
/*       </ul>*/
/*       {% endif %}</li>*/
/*     {% set i = i + 1 %}*/
/*     {% endfor %}*/
/*   </ul>*/
/*   <div id="stats">*/
/*     <ul>*/
/*       <li>*/
/*         <div>{{ text_complete_status }} <span class="pull-right">{{ complete_status }}%</span></div>*/
/*         <div class="progress">*/
/*           <div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="{{ complete_status }}" aria-valuemin="0" aria-valuemax="100" style="width: {{ complete_status }}%"> <span class="sr-only">{{ complete_status }}%</span></div>*/
/*         </div>*/
/*       </li>*/
/*       <li>*/
/*         <div>{{ text_processing_status }} <span class="pull-right">{{ processing_status }}%</span></div>*/
/*         <div class="progress">*/
/*           <div class="progress-bar progress-bar-warning" role="progressbar" aria-valuenow="{{ processing_status }}" aria-valuemin="0" aria-valuemax="100" style="width: {{ processing_status }}%"> <span class="sr-only">{{ processing_status }}%</span></div>*/
/*         </div>*/
/*       </li>*/
/*       <li>*/
/*         <div>{{ text_other_status }} <span class="pull-right">{{ other_status }}%</span></div>*/
/*         <div class="progress">*/
/*           <div class="progress-bar progress-bar-danger" role="progressbar" aria-valuenow="{{ other_status }}" aria-valuemin="0" aria-valuemax="100" style="width: {{ other_status }}%"> <span class="sr-only">{{ other_status }}%</span></div>*/
/*         </div>*/
/*       </li>*/
/*     </ul>*/
/*   </div>*/
/* </nav>*/
/* */
