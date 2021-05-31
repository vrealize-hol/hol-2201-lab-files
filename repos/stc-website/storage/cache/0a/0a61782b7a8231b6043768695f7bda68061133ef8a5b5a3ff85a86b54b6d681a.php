<?php

/* default/template/extension/module/featured.twig */
class __TwigTemplate_9c3970c7a224b048362fbf3bfcbb76611f1bb55f43eba7cafbf83c73964dea18 extends Twig_Template
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
        echo "<h3>";
        echo (isset($context["heading_title"]) ? $context["heading_title"] : null);
        echo "</h3>
<div class=\"row\">";
        // line 3
        $context['_parent'] = $context;
        $context['_seq'] = twig_ensure_traversable((isset($context["products"]) ? $context["products"] : null));
        foreach ($context['_seq'] as $context["_key"] => $context["product"]) {
            // line 4
            echo "  <div class=\"product-layout col-lg-3 col-md-3 col-sm-6 col-xs-12\">
    <div class=\"product-thumb transition\">
      <div class=\"image\"><a href=\"";
            // line 6
            echo $this->getAttribute($context["product"], "href", array());
            echo "\"><img src=\"";
            echo $this->getAttribute($context["product"], "thumb", array());
            echo "\" alt=\"";
            echo $this->getAttribute($context["product"], "name", array());
            echo "\" title=\"";
            echo $this->getAttribute($context["product"], "name", array());
            echo "\" class=\"img-responsive\" /></a></div>
      <div class=\"caption\">
        <h4><a href=\"";
            // line 8
            echo $this->getAttribute($context["product"], "href", array());
            echo "\">";
            echo $this->getAttribute($context["product"], "name", array());
            echo "</a></h4>
        <p>";
            // line 9
            echo $this->getAttribute($context["product"], "description", array());
            echo "</p>";
            // line 10
            if ($this->getAttribute($context["product"], "rating", array())) {
                // line 11
                echo "        <div class=\"rating\">";
                // line 12
                $context['_parent'] = $context;
                $context['_seq'] = twig_ensure_traversable(5);
                foreach ($context['_seq'] as $context["_key"] => $context["i"]) {
                    // line 13
                    if (($this->getAttribute($context["product"], "rating", array()) < $context["i"])) {
                        // line 14
                        echo "          <span class=\"fa fa-stack\"><i class=\"fa fa-star-o fa-stack-2x\"></i></span>";
                    } else {
                        // line 16
                        echo "          <span class=\"fa fa-stack\"><i class=\"fa fa-star fa-stack-2x\"></i><i class=\"fa fa-star-o fa-stack-2x\"></i></span>";
                    }
                }
                $_parent = $context['_parent'];
                unset($context['_seq'], $context['_iterated'], $context['_key'], $context['i'], $context['_parent'], $context['loop']);
                $context = array_intersect_key($context, $_parent) + $_parent;
                // line 19
                echo "        </div>";
            }
            // line 21
            if ($this->getAttribute($context["product"], "price", array())) {
                // line 22
                echo "        <p class=\"price\">";
                // line 23
                if ( !$this->getAttribute($context["product"], "special", array())) {
                    // line 24
                    echo $this->getAttribute($context["product"], "price", array());
                } else {
                    // line 26
                    echo "          <span class=\"price-new\">";
                    echo $this->getAttribute($context["product"], "special", array());
                    echo "</span> <span class=\"price-old\">";
                    echo $this->getAttribute($context["product"], "price", array());
                    echo "</span>";
                }
                // line 28
                if ($this->getAttribute($context["product"], "tax", array())) {
                    // line 29
                    echo "          <span class=\"price-tax\">";
                    echo (isset($context["text_tax"]) ? $context["text_tax"] : null);
                    echo $this->getAttribute($context["product"], "tax", array());
                    echo "</span>";
                }
                // line 31
                echo "        </p>";
            }
            // line 33
            echo "      </div>
      <div class=\"button-group\">
        <button type=\"button\" onclick=\"cart.add('";
            // line 35
            echo $this->getAttribute($context["product"], "product_id", array());
            echo "');\"><i class=\"fa fa-shopping-cart\"></i> <span class=\"hidden-xs hidden-sm hidden-md\">";
            echo (isset($context["button_cart"]) ? $context["button_cart"] : null);
            echo "</span></button>
        <button type=\"button\" data-toggle=\"tooltip\" title=\"";
            // line 36
            echo (isset($context["button_wishlist"]) ? $context["button_wishlist"] : null);
            echo "\" onclick=\"wishlist.add('";
            echo $this->getAttribute($context["product"], "product_id", array());
            echo "');\"><i class=\"fa fa-heart\"></i></button>
        <button type=\"button\" data-toggle=\"tooltip\" title=\"";
            // line 37
            echo (isset($context["button_compare"]) ? $context["button_compare"] : null);
            echo "\" onclick=\"compare.add('";
            echo $this->getAttribute($context["product"], "product_id", array());
            echo "');\"><i class=\"fa fa-exchange\"></i></button>
      </div>
    </div>
  </div>";
        }
        $_parent = $context['_parent'];
        unset($context['_seq'], $context['_iterated'], $context['_key'], $context['product'], $context['_parent'], $context['loop']);
        $context = array_intersect_key($context, $_parent) + $_parent;
        // line 42
        echo "</div>
";
    }

    public function getTemplateName()
    {
        return "default/template/extension/module/featured.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  130 => 42,  118 => 37,  112 => 36,  106 => 35,  102 => 33,  99 => 31,  93 => 29,  91 => 28,  84 => 26,  81 => 24,  79 => 23,  77 => 22,  75 => 21,  72 => 19,  65 => 16,  62 => 14,  60 => 13,  56 => 12,  54 => 11,  52 => 10,  49 => 9,  43 => 8,  32 => 6,  28 => 4,  24 => 3,  19 => 1,);
    }
}
/* <h3>{{ heading_title }}</h3>*/
/* <div class="row">*/
/*  {% for product in products %}*/
/*   <div class="product-layout col-lg-3 col-md-3 col-sm-6 col-xs-12">*/
/*     <div class="product-thumb transition">*/
/*       <div class="image"><a href="{{ product.href }}"><img src="{{ product.thumb }}" alt="{{ product.name }}" title="{{ product.name }}" class="img-responsive" /></a></div>*/
/*       <div class="caption">*/
/*         <h4><a href="{{ product.href }}">{{ product.name }}</a></h4>*/
/*         <p>{{ product.description }}</p>*/
/*         {% if product.rating %}*/
/*         <div class="rating">*/
/*           {% for i in 5 %}*/
/*           {% if product.rating < i %}*/
/*           <span class="fa fa-stack"><i class="fa fa-star-o fa-stack-2x"></i></span>*/
/*           {% else %}*/
/*           <span class="fa fa-stack"><i class="fa fa-star fa-stack-2x"></i><i class="fa fa-star-o fa-stack-2x"></i></span>*/
/*           {% endif %}*/
/*           {% endfor %}*/
/*         </div>*/
/*         {% endif %}*/
/*         {% if product.price %}*/
/*         <p class="price">*/
/*           {% if not product.special %}*/
/*           {{ product.price }}*/
/*           {% else %}*/
/*           <span class="price-new">{{ product.special }}</span> <span class="price-old">{{ product.price }}</span>*/
/*           {% endif %}*/
/*           {% if product.tax %}*/
/*           <span class="price-tax">{{ text_tax }} {{ product.tax }}</span>*/
/*           {% endif %}*/
/*         </p>*/
/*         {% endif %}*/
/*       </div>*/
/*       <div class="button-group">*/
/*         <button type="button" onclick="cart.add('{{ product.product_id }}');"><i class="fa fa-shopping-cart"></i> <span class="hidden-xs hidden-sm hidden-md">{{ button_cart }}</span></button>*/
/*         <button type="button" data-toggle="tooltip" title="{{ button_wishlist }}" onclick="wishlist.add('{{ product.product_id }}');"><i class="fa fa-heart"></i></button>*/
/*         <button type="button" data-toggle="tooltip" title="{{ button_compare }}" onclick="compare.add('{{ product.product_id }}');"><i class="fa fa-exchange"></i></button>*/
/*       </div>*/
/*     </div>*/
/*   </div>*/
/*   {% endfor %}*/
/* </div>*/
/* */
