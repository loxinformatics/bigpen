# @login_required
# def place_order(request):
#     if request.method == "POST":
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = Order.objects.create(user=request.user)
#             for item in Item.objects.all():
#                 quantity = form.cleaned_data.get(f"item_{item.id}")
#                 if quantity and quantity > 0:
#                     OrderItem.objects.create(order=order, item=item, quantity=quantity)
#                     # Subtract from stock
#                     item.quantity -= quantity
#                     item.save()
#             return redirect("order_success")  # Make sure this exists
#     else:
#         form = OrderForm()

#     return render(request, "shop/place_order.html", {"form": form})
