/**
 * @module       Carousel with orbital pagination
 * @author       ATOM
 * @license      MIT
 * @version      v1.0.1
 */

 console.clear();

 // Core
 function initCarousel( options ) {
     function CustomCarousel( options ) {
         this.init( options );
         this.addListeners();
         return this;
     }
 
     CustomCarousel.prototype.init = function ( options ) {
         this.node        = options.node;
         this.node.slider = this;
         this.slides      = this.node.querySelector( '.slides' ).children;
         this.slidesN     = this.slides.length;
         this.pagination  = this.node.querySelector( '.pagination' );
         this.pagTransf   = 'translate( -50%, -50% )';
         this.dots        = this.pagination.children;
         this.dotsN       = this.dots.length;
         this.step        = -360/this.dotsN;
         this.angle       = 0;
         this.next        = this.node.querySelector( '.next' );
         this.prev        = this.node.querySelector( '.prev' );
         this.activeN     = options.activeN || 0;
         this.prevN       = this.activeN;
         this.speed       = options.speed || 300;
         this.autoplay    = options.autoplay || false;
         this.autoplayId  = null;
 
         this.setSlide( this.activeN );
         this.arrangeDots();
         this.pagination.style.transitionDuration = this.speed +'ms';
         if ( this.autoplay ) this.startAutoplay();
     }
 
     CustomCarousel.prototype.addListeners = function () {
         var slider = this;
 
         if ( this.next ) {
             this.next.addEventListener( 'click', function() {
                 slider.setSlide( slider.activeN + 1 );
             });
         }
 
         if ( this.prev ) {
             this.prev.addEventListener( 'click', function() {
                 slider.setSlide( slider.activeN - 1 );
             });
         }
 
         for ( var i = 0; i < this.dots.length; i++ ) {		
             this.dots[i].addEventListener( 'click', function( i ) {
                 return function() { slider.setSlide( i ); }
             }( i ));
         }
     };
 
     CustomCarousel.prototype.setSlide = function ( slideN ) {
         this.slides[ this.activeN ].classList.remove( 'active' );
         if ( this.dots[ this.activeN ] ) this.dots[ this.activeN ].classList.remove( 'active' );
 
         this.prevN = this.activeN;
         this.activeN = slideN;
         if ( this.activeN < 0 ) this.activeN = this.slidesN -1;
         else if ( this.activeN >= this.slidesN ) this.activeN = 0;
 
         this.slides[ this.activeN ].classList.toggle( 'active' );	
         if ( this.dots[ this.activeN ] ) this.dots[ this.activeN ].classList.toggle( 'active' );
 
         this.rotate();
     };
 
     CustomCarousel.prototype.rotate = function () {
         if ( this.activeN < this.dotsN ) {
             this.angle += function ( dots, next, prev, step ) {
                 var inc, half = dots/2;
                 if( prev > dots ) prev = dots - 1;
                 if( Math.abs( inc = next - prev ) <= half ) return step * inc;
                 if( Math.abs( inc = next - prev + dots ) <= half ) return step * inc;
                 if( Math.abs( inc = next - prev - dots ) <= half ) return step * inc;
             }( this.dotsN, this.activeN, this.prevN, this.step )
 
             this.pagination.style.transform = this.pagTransf +'rotate('+ this.angle +'deg)';
         }
     };
 
     CustomCarousel.prototype.startAutoplay = function () {
         var slider = this;
 
         this.autoplayId = setInterval( function(){
             slider.setSlide( slider.activeN + 1 );
         }, this.autoplay );
     };
 
     CustomCarousel.prototype.stopAutoplay = function () {
         clearInterval( this.autoplayId );
     };
 
     CustomCarousel.prototype.arrangeDots = function () {
         for ( var i = 0; i < this.dotsN; i++ ) {
             this.dots[i].style.transform = 'rotate('+ 360/this.dotsN * i +'deg)';
         }
     };
     
     return new CustomCarousel( options );
 }
 
 
 // Init
 var plugins = {
     customCarousel: document.querySelectorAll( '.circle-carousel' )
 }
 
 document.addEventListener( 'DOMContentLoaded', function() {
     if( plugins.customCarousel.length ) {
         for ( var i = 0; i < plugins.customCarousel.length; i++ ) {
             var carousel = initCarousel({
                 node: plugins.customCarousel[i],
                 speed: plugins.customCarousel[i].getAttribute( 'data-speed' ),
                 autoplay: plugins.customCarousel[i].getAttribute( 'data-autoplay' )
             });
         }
     }
 });
 