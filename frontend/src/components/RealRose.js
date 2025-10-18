import React from 'react';
import './RealRose.css';

function RealRose({ show }) {
  if (!show) return null;
  
  return (
    <div className="real-rose-overlay">
      <div className="real-rose-container">
        <div className="light-red light1"></div>
        <div className="light-red light2"></div>
        <div className="light-red light3"></div>
        
        <div className="particle-red particle1"></div>
        <div className="particle-red particle2"></div>
        <div className="particle-red particle3"></div>
        <div className="particle-red particle4"></div>
        <div className="particle-red particle5"></div>

        <div className="rose-wrapper-real">
          <div className="stem-real">
            <div className="thorn-real thorn1"></div>
            <div className="thorn-real thorn2"></div>
            <div className="thorn-real thorn3"></div>
          </div>
          <div className="leaf-real left-real"></div>
          <div className="leaf-real right-real"></div>
          
          <div className="rose-real">
            {/* Pétalos externos */}
            <div className="petal-outer-real petal-outer1-real"></div>
            <div className="petal-outer-real petal-outer2-real"></div>
            <div className="petal-outer-real petal-outer3-real"></div>
            <div className="petal-outer-real petal-outer4-real"></div>
            <div className="petal-outer-real petal-outer5-real"></div>
            <div className="petal-outer-real petal-outer6-real"></div>
            
            {/* Pétalos medios */}
            <div className="petal-mid-real petal-mid1-real"></div>
            <div className="petal-mid-real petal-mid2-real"></div>
            <div className="petal-mid-real petal-mid3-real"></div>
            <div className="petal-mid-real petal-mid4-real"></div>
            <div className="petal-mid-real petal-mid5-real"></div>
            <div className="petal-mid-real petal-mid6-real"></div>
            
            {/* Pétalos internos */}
            <div className="petal-inner-real petal-inner1-real"></div>
            <div className="petal-inner-real petal-inner2-real"></div>
            <div className="petal-inner-real petal-inner3-real"></div>
            <div className="petal-inner-real petal-inner4-real"></div>
            <div className="petal-inner-real petal-inner5-real"></div>
            <div className="petal-inner-real petal-inner6-real"></div>
            
            <div className="center-real"></div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RealRose;
