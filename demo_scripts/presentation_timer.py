#!/usr/bin/env python3
"""
PRESENTATION TIMER
Giúp bạn kiểm soát thời gian khi demo
"""

import time
import sys
from datetime import datetime, timedelta

class PresentationTimer:
    def __init__(self, total_minutes=15):
        self.total_minutes = total_minutes
        self.segments = [
            ("Introduction", 0.5),
            ("Dataset Overview", 2.0),
            ("Training Results", 3.0),
            ("Live Prediction", 4.0),
            ("Visualization", 2.0),
            ("Q&A", 3.0),
            ("Wrap-up", 0.5)
        ]
        
    def run(self):
        print("="*50)
        print("   PRESENTATION TIMER - 15 MINUTES")
        print("="*50)
        print("\nPress Enter to start each segment...")
        print("Press Ctrl+C to stop\n")
        
        start_time = None
        current_segment = 0
        
        try:
            for i, (segment_name, duration) in enumerate(self.segments):
                print(f"\n[{i+1}/{len(self.segments)}] {segment_name} ({duration} min)")
                print("-" * 40)
                
                if i == 0:
                    input("Press Enter to START presentation...")
                    start_time = datetime.now()
                else:
                    input("Press Enter to start this segment...")
                
                segment_start = datetime.now()
                segment_end = segment_start + timedelta(minutes=duration)
                
                while datetime.now() < segment_end:
                    remaining = (segment_end - datetime.now()).total_seconds()
                    elapsed_total = (datetime.now() - start_time).total_seconds() / 60
                    
                    if remaining < 30 and remaining > 29:
                        print("\n⚠️  30 seconds remaining for this segment!")
                    
                    mins, secs = divmod(int(remaining), 60)
                    print(f"\r⏱️  Segment: {mins:02d}:{secs:02d} | "
                          f"Total: {elapsed_total:.1f}/{self.total_minutes} min", 
                          end="", flush=True)
                    
                    time.sleep(1)
                
                print(f"\n✓ {segment_name} completed!")
                
                if i < len(self.segments) - 1:
                    print("Ready for next segment...")
                
            print("\n\n🎉 PRESENTATION COMPLETED!")
            total_time = (datetime.now() - start_time).total_seconds() / 60
            print(f"Total time: {total_time:.1f} minutes")
            
            if total_time > self.total_minutes:
                print(f"⚠️  Overtime by {total_time - self.total_minutes:.1f} minutes")
            else:
                print(f"✓ {self.total_minutes - total_time:.1f} minutes to spare!")
                
        except KeyboardInterrupt:
            print("\n\nTimer stopped by user.")

def practice_mode():
    """Chế độ luyện tập với feedback"""
    print("\n🎯 PRACTICE MODE")
    print("="*50)
    print("I'll give you topics to present. Try to match the target time!\n")
    
    topics = [
        ("Explain the dataset", 60),
        ("Describe the 4 algorithms", 90),
        ("Show prediction demo", 120),
        ("Explain the results", 60)
    ]
    
    for topic, target_seconds in topics:
        print(f"\n📢 Topic: {topic}")
        print(f"⏱️  Target time: {target_seconds} seconds")
        input("Press Enter when ready to start...")
        
        start = time.time()
        input("Press Enter when done...")
        elapsed = time.time() - start
        
        diff = abs(elapsed - target_seconds)
        if diff < 5:
            print(f"✅ Excellent! {elapsed:.1f}s (target: {target_seconds}s)")
        elif diff < 10:
            print(f"✓ Good! {elapsed:.1f}s (target: {target_seconds}s)")
        else:
            if elapsed < target_seconds:
                print(f"⚡ Too fast! {elapsed:.1f}s (target: {target_seconds}s)")
            else:
                print(f"🐌 Too slow! {elapsed:.1f}s (target: {target_seconds}s)")

if __name__ == "__main__":
    print("Choose mode:")
    print("1. Presentation Timer (15 min)")
    print("2. Practice Mode")
    
    choice = input("\nEnter choice (1-2): ")
    
    if choice == '1':
        timer = PresentationTimer()
        timer.run()
    elif choice == '2':
        practice_mode()
    else:
        print("Invalid choice!")