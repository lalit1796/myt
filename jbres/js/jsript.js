!function(w,d,b,$){

	var thisaput={
	el:function(e){
		return $(e)
		},
	ck:{
		mx:function(a,b){
			
			return (a>b)?a:b;
		},
		sm:function(a,b){
			if(a===b){return true}else{return false}
		}
	},
	cd:function(e,i,c){
		el=d.createElement(e);
		if(!this.ck.sm(typeof i,"undefined")){el.id=i;}
		if(!this.ck.sm(typeof c,"undefined")){el.classList.add(c);}
		return el;
	},
	jpan:{
		jclass:{
			jact_:"activity",
			jglob_:"place"
			},
		jtrig:function(){

		
			
				thisaput.el(".jtrig").click(function(e){
					e.preventDefault();
					
					$(document).mousedown(function(e){
						var cn = $(".jtrig,.bhgon")
						if(!cn.is(e.target) && cn.has(e.target).length === 0){
							$("#jclose").click();// more menu
						}
					
					});
					
					if($(this).hasClass("jclick") && $("#_jpan").hasClass("jopen")){
						thisaput.el("#jclose").click();
					}
					else{
					$(".jtrig").removeClass("jclick");	
					$(this).addClass('jclick');
					$("#_jpan").addClass("jopen");
					$("#explorer,#tours,#search").addClass("hide");
					switch($(this).data("rep")){
						case "jglob":
							$("#explorer").removeClass("hide");
						break;
						case "jact": 
							$("#tours").removeClass("hide");
						break;
						case "jserc":
							console.log("hit")
							$("#search").removeClass("hide");
						break;
						default:;
						}
					}
					
				});
					
				thisaput.el("#jclose").click(function(){
					$(".jtrig").removeClass("jclick");
					$("#_jpan").removeClass("jopen");
					
				});
				
				
			
			
			
		},
		ini:function(){
			// first add a class saying it clicked.
			// then using that if contain condition check the button clicked;
			this.jtrig();
		}
	},
	
	body:{
		
		noscroll :function(){
			thisaput.el("body").addClass("noscroll");
			$('body').bind('touchmove', function(e){e.preventDefault()})
		},
		resumescroll :  function(){
			thisaput.el("body").removeClass("noscroll");
			$('body').unbind('touchmove');
			
		}
		
	},
	
	query:{
		
		propre:function(){
			console.log("made");
		},
		
		fthis:function(){
			thisaput.el(".qrybtn").click(function(e){
				e.preventDefault();
				
					
					t=$(this);
					el=$("#enqcrok");
					el.html("");
					el.append("<input type='hidden' value='"+t.data('p')+"' name='prod'/>");
					el.append("<input type='hidden' value='"+t.data("id")+"' name='id'/>");
					el.append("<input type='hidden' value='"+t.attr("href")+"' name='url'/>");
					
				
				
				setTimeout(
				
				function(){
					
				thisaput.el("#sashdoc").html($(this).data('id')+$(this).data("title"));
				thisaput.body.noscroll();
				thisaput.el("#enqFormModal").addClass("ppno");
				
				}
				,200)
					
				
				
				
				
			});
		},
		cbt:function(){
			thisaput.el("#formterm").click(function(){
				thisaput.body.resumescroll();
				thisaput.el("#enqFormModal").removeClass("ppno");
			});
		},
		ini:function(){
			this.fthis();
			this.cbt();
		}
	},
	
	forms:{
		
		propre:function(e){
				$("form[method=POST]").submit(function(e){
					if($(this).data('through')!="1"){
						e.preventDefault();
						f = $(this);
						d=$.param($(this).serializeArray());
						var post = $.ajax({
							type: "POST",
							url: this.action,
							data: d,
							error: function(XMLHttpRequest, textStatus, errorThrown){
								console.log(XMLHttpRequest, textStatus, errorThrown);
								thisaput.body.resumescroll();
									$("#enqcrok").html("");
									$("form[method=POST]").trigger("reset")
									.find(":input").prop("disabled", false);	
								     setTimeout(function(){
										thisaput.forms.modal("<span class='err'>Some error occured! We are on it...</span>");
									 },500)
								},
								
							beforeSend: function(jqXHR,setting){
									
									f.find(":input").prop("disabled", true);
									thisaput.forms.modal("<div class='loading'></div>",true);
									
									
							}
							
							}).done(
								function(msg){
									//console.log(msg)
									
									$("#enqcrok").html("");
									$("form[method=POST]").trigger("reset")
									.find(":input").prop("disabled", false);
									var response = msg.replace(/\s/g,"");
									
									if( response== "success"){
										location.reload();
									}
									else if(response=="failed"){
										f.find(":input").prop("disabled", false);
										$("#responselg").html("<span style='color:red'>Please enter the correct username and password.</span>");
										thisaput.forms.modal("Snap! login failed.",false);
										$(".fetching-").hide();
									}
									else if(response=="pnm"){
										f.find(":input").prop("disabled", false);
										$("#responselg-").html("<span style='color:red'>Passwords do not match.</span>");
										thisaput.forms.modal("Invalid password.",false);
										$(".fetching-").hide();
									}
									else if(response=="uct"){
										f.find(":input").prop("disabled", false);
										$("#responselg-").html("<span style='color:green'>Account is created. Please login to continue.</span>");
										thisaput.forms.modal("Greetings! your account has been created. Login to continue...",false);
										$(".fetching-").hide();
									}
									else if(response=="axt"){
										f.find(":input").prop("disabled", false);
										$("#responselg-").html("<span style='color:red'>You already have account for this email.</span>");
										thisaput.forms.modal("You already have account for this email. Click forget password to recover password.",false);
										$(".fetching-").hide();
									}
									
									else if(response=="enq_sub"){
										thisaput.body.resumescroll();
										thisaput.forms.modal("Hey! Your request has been submitted. You will be contacted soon...",false);
									} 
									else{
										thisaput.body.resumescroll();
										console.log(response);
										thisaput.forms.modal(response,false);
										
									}
										
									
								
								
								}); 
					}
					else {
						
						if($(this).data('log')=="1"){
							f = $(this);
							if(!_usrPipe()){
									
									e.preventDefault();
									$(".logger").click();
									thisaput.forms.modal("<div class=''>You must login first.</div>",false);
									
								}
									
							
						}
						
					}	
					
					//ajax
						
						
				});
			
			
			
			
		},
		fthis:function(){
			thisaput.el(".logger ").click(function(e){
				e.preventDefault();
				setTimeout(
					function(){thisaput.body.noscroll();thisaput.el("#logblock").removeClass("hidden");}
				,200);
			});
			
		},
		cbt:function(){
			thisaput.el("#logdisperse").click(function(){
				
				thisaput.body.resumescroll();
				thisaput.el("#logblock").addClass("hidden");
			});
		},
		modal:function(msg,auto){
			
			if(auto){$("#closeBtn").hide();}
			else{$("#closeBtn").show();$(".ppno").removeClass("ppno");}
			
			thisaput.body.noscroll();
			
			$("#enqmodal").addClass("ppno")
			$("#response_enq").html(msg);
			$("#closeBtn").click(function(){
				$(".ppno").removeClass("ppno");
				thisaput.body.resumescroll();
			});
			
			
			
		},
		ini:function(){
			this.fthis();
			this.cbt();
			this.propre();
		}
	},
	
	
			
	ini:function(){
		// THE first initialisation...

		this.jpan.ini();
		this.query.ini();
		this.forms.ini();
		
		//console.log($("form[method=POST]"));
		
		
		//console.log( thisaput.cd("div","i","c") )
			
	}
	
	
	
	
	
}

	
	
thisaput.ini();	
	
	
	
}(window,document,document.body,$)




//jqueries

$(document).ready(function(){
		
		
		$(".x-container").each(function(){if(($(this).children("p,.ilist")).length<3)$(this).siblings(".shomo").html("")})
		//$(".x-container").each(function(){if(($(this).children("p")).length<3)$(this).siblings(".shomo").html("")})
		
		$(".shomobtn").click(function(){
			
			
			s = $(this).parent().siblings(".x-container");
			if(s.hasClass("mini")){s.removeClass("mini");$(this).html("Show less");$(this).siblings(".rooter").addClass("rot");}
			else{s.addClass("mini");$(this).html("Expand");$(this).siblings(".rooter").removeClass("rot");}
		});
		
		// navpop
			$(window).scroll(function(){
				if($(this).scrollTop()>100){
					$(".navinsite").addClass("navdown");
				}
				else{
						$(".navinsite").removeClass("navdown");

				}
			});
			
			$("#pop-mor-btn").click(function(e){
			e.preventDefault();
			setTimeout(function(){
			
				if($("#pop-mor").hasClass("open")){
					$("#pop-mor").removeClass("open");
					$("#pop-mor-btn").removeClass("pop-mor-click");
				}
				else{
					$("#pop-mor").addClass("open");
					$("#pop-mor-btn").addClass("pop-mor-click");
				}
			
			},200)
				
			});
		
			
	})
	
	
	.trigger("scroll")
	
	.mousedown(function(e){
		var cn = $("#pop-mor,#pop-mor-btn")
		if(!cn.is(e.target) && cn.has(e.target).length === 0){
			$("#pop-mor").removeClass("open");// more menu
			$("#pop-mor-btn").removeClass("pop-mor-click");
		}
	})
		










//carousal

$(document).ready(function(){
											items=$("._crul_").children();
											//items.last().addClass("prev");
											//items.first().addClass("selected");
											//items.first().next().addClass("next");
											
											var slider;
											
											//next
											$("#btn-n").click(function(){
											
											
													if(items.length>=3){
													//console.log(items.last().length)
													
													items.each(function(i){
														cur = $(this)
														//console.log(cur);
														if(cur.hasClass("selected")){
															//console.log(cur);
															items.removeClass("selected");
															items.removeClass("next");
															items.removeClass("prev");
															if(cur.next().length==0){
																items.last().addClass("prev");
																items.first().addClass("selected");
																items.first().next().addClass("next");
															}
															else{
															//console.log("2")
																cur.addClass("prev");
																cur.next().addClass("selected");
																	if(cur.next().next().length==0){
																		items.first().addClass("next");
																	}
																	else{
																		cur.next().next().addClass("next");
																	}
																
															}
															return false;	
														}
													});
													
													
												}
												
											
											
											});
											
											
											//prev
											
											$("#btn-p").click(function(){
											
											
													if(items.length>=3){
													//console.log(items.last().length)
													
													items.each(function(i){
														cur = $(this)
														//console.log(cur);
														if(cur.hasClass("selected")){
															//console.log(cur);
															items.removeClass("selected");
															items.removeClass("next");
															items.removeClass("prev");
															if(cur.prev().length==0){
																items.last().prev().addClass("prev");
																items.last().addClass("selected");
																items.first().addClass("next");
															}
															else{
															console.log("2")
																cur.addClass("next");
																cur.prev().addClass("selected");
																	if(cur.prev().prev().length==0){
																		items.last().addClass("prev");
																	}
																	else{
																		cur.prev().prev().addClass("prev");
																	}
																
															}
															return false;	
														}
													});
													
													
												}
												
											
											
											});
											
											$("#feurate").hover(
													function(){clearInterval(slider);$(".fetue-txt").show();},
													function(){
													$(".fetue-txt").hide();
													slider =  setInterval(function(){$("#btn-n").click();},5000);}
													).trigger("mouseleave");
													
											
										});