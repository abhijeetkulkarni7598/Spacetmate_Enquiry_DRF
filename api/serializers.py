from rest_framework import serializers

from api.models import *

#create serializers here







class ItemSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(required=False)
    class Meta:
        model=Item
        fields="__all__"
        read_only_fields=('quotation',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Status
        fields="__all__"

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Items
        fields="__all__"


class QuotationSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=True,read_only=False)


    class Meta:
        model=Quotation
        fields="__all__"
        # exclude = ['user']
    
    def update(self, instance, validated_data):
        item_data = validated_data.pop('item', None)

        # Update the Quotation instance fields
        instance.quotation_number = validated_data.get('quotation_number', instance.quotation_number)
        instance.user_client = validated_data.get('user_client', instance.user_client)
        # Update other fields similarly...
        for field_name, value in validated_data.items():
            setattr(instance, field_name, value)
        # Save the updated Quotation instance
        instance.save()

        if item_data is not None:
            current_item_ids = [item['id'] for item in item_data if 'id' in item]

            # Delete items not present in the updated data
            for item in instance.item.all():
                if item.id not in current_item_ids:
                    item.delete()

            # Update or create each Item related to this Quotation
            for item in item_data:
                item_id = item.get('id', None)
                if item_id:
                    # If Item exists, update it
                    item_instance = Item.objects.get(id=item_id)
                    ItemSerializer().update(item_instance, item)
                else:
                    # If Item doesn't exist, create it
                    Item.objects.create(quotation=instance, **item)

        return instance
    
    def create(self,validated_data):
        item=validated_data.pop('item')
        quotation=Quotation.objects.create(**validated_data)

        for choice in item:
            Item.objects.create(**choice,quotation=quotation)

        return quotation

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=InteriorGallery
        fields='__all__'
class DesignGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model=DesignGallery
        fields='__all__'











class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Client
        fields="__all__"



class InventorysSerializer(serializers.ModelSerializer):
    class Meta:
        model=Inventorys
        fields='__all__'